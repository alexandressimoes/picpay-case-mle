import asyncio
from datetime import datetime
import shutil
import spacy
from pathlib import Path
import json
import threading
from typing import Dict, Any
from spacy.util import is_package
import logging

logger = logging.getLogger(__name__)
# REGISTRY_FILE = MODELS_DIR / "registry.json"


class ModelManager:
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_models: dict[str, spacy.Language] = {}
        self._io_lock = threading.Lock()
        self._async_lock = asyncio.Lock()
        self.model_registry = self._load_model_registry()
        self.model_registry_file = self.models_dir / "model_registry.json"
        self.predictions_registry_file = self.models_dir / "predictions_registry.json"

    def _load_model_registry(self) -> dict:
        """Reads the list of downloaded models and the last used model from JSON."""
        if (self.models_dir / "model_registry.json").exists():
            with open(self.models_dir / "model_registry.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"downloaded_models": [], "last_used_model": None}

    def _save_model_registry(self, model_name: str) -> None:
        """Saves the list of downloaded models and the last used model to JSON."""
        with self._io_lock:
            if not self.model_registry_file.exists():
                with open(self.model_registry_file, "w", encoding="utf-8") as f:
                    json.dump({"downloaded_models": [], "last_used_model": None}, f, indent=2)

            # 2. Registra se for um modelo novo baixado
            if model_name not in self.model_registry["downloaded_models"]:
                self.model_registry["downloaded_models"].append(model_name)

            # 3. Atualiza o último modelo utilizado e salva o JSON
            self.model_registry["last_used_model"] = model_name

            with open(self.model_registry_file, "w", encoding="utf-8") as f:
                json.dump(self.model_registry, f, indent=2)

        

    def load_model(self, model_name: str) -> spacy.Language:
        """
        Downloads and loads a spaCy model. If the model is already downloaded, it will be loaded from disk.
        If the model is new, it will be downloaded, saved to disk, and registered in the registry. 
        The last used model will also be updated in the registry.
        """
        model_path = self.models_dir / model_name

        # 1. Baixa o modelo caso não esteja na pasta local
        if not model_path.exists():
            if not is_package(model_name):
                logger.info(f"Baixando modelo {model_name}...")
                spacy.cli.download(model_name)

            nlp = spacy.load(model_name)
            logger.info(f"Salvando o modelo em {model_path}...")
            nlp.to_disk(model_path)
            
        else:
            logger.info(f"Carregando modelo diretamente da pasta local {model_path}...")
            nlp = spacy.load(model_path)

        self._save_model_registry(model_name)

        # 4. Mantém carregado em memória
        self.loaded_models[model_name] = nlp
        return nlp

    def delete_model(self, model_name: str) -> None:
        """Removes a model from disk, memory cache, and the registry."""
        with self._io_lock:
            model_path = self.models_dir / model_name

            if not model_path.exists() and model_name not in self.model_registry["downloaded_models"]:
                raise ValueError(f"O modelo '{model_name}' não foi encontrado localmente.")

            if model_path.exists():
                shutil.rmtree(model_path)

            self.loaded_models.pop(model_name, None)

            if model_name in self.model_registry["downloaded_models"]:
                self.model_registry["downloaded_models"].remove(model_name)

            if self.model_registry.get("last_used_model") == model_name:
                self.model_registry["last_used_model"] = None

            with open(self.model_registry_file, "w", encoding="utf-8") as f:
                json.dump(self.model_registry, f, indent=2)

    def _save_prediction_registry(self, payload: Dict[str, Any]):
        """Register the prediction made in a JSON file.
        """
        with self._io_lock:
            if not self.predictions_registry_file.exists():
                with open(self.predictions_registry_file, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)

            with open(self.predictions_registry_file, "r", encoding="utf-8") as f:
                predictions = json.load(f)

            predictions.append(payload)

            with open(self.predictions_registry_file, "w", encoding="utf-8") as f:
                json.dump(predictions, f, indent=2)


    def predict(self, text: str, model_name: str | None = None) -> dict[str, Any]:
        """Realiza a inferência usando o modelo solicitado ou o último carregado."""
        target_model = model_name or self.model_registry.get("last_used_model")

        if not target_model:
            raise ValueError("Nenhum modelo foi carregado ainda. Chame a rota /load/ primeiro.")

        # Se o modelo já foi baixado antes mas não está na RAM, carrega do disco
        if target_model not in self.loaded_models:
            if target_model in self.model_registry["downloaded_models"]:
                self.load_model(target_model)
            else:
                raise ValueError(f"O modelo '{target_model}' não foi encontrado localmente.")

        # Realiza a inferência
        nlp = self.loaded_models[target_model]
        doc = nlp(text)
        transaction_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        prediction_entities = {ent.label_: ent.text for ent in doc.ents}

        # Registra a predição
        payload_return = {"input": text, 
                          "output": prediction_entities, 
                          "model_name": target_model,
                          "timestamp": transaction_timestamp}
        self._save_prediction_registry(payload_return)

        return payload_return

    def list_predictions(self) -> list[dict[str, Any]]:
        with self._io_lock:
            if not self.predictions_registry_file.exists():
                return []

            with open(self.predictions_registry_file, "r", encoding="utf-8") as f:
                return json.load(f)

    def get_model_registry(self) -> dict[str, Any]:
        with self._io_lock:
            return {
                "downloaded_models": list(self.model_registry.get("downloaded_models", [])),
                "last_used_model": self.model_registry.get("last_used_model"),
            }

    async def load_model_async(self, model_name: str) -> spacy.Language:
        async with self._async_lock:
            return await asyncio.to_thread(self.load_model, model_name)

    async def predict_async(self, text: str, model_name: str | None = None) -> dict[str, Any]:
        return await asyncio.to_thread(self.predict, text, model_name)

    async def delete_model_async(self, model_name: str) -> None:
        async with self._async_lock:
            await asyncio.to_thread(self.delete_model, model_name)

    async def list_predictions_async(self) -> list[dict[str, Any]]:
        return await asyncio.to_thread(self.list_predictions)

    async def get_model_registry_async(self) -> dict[str, Any]:
        return await asyncio.to_thread(self.get_model_registry)
