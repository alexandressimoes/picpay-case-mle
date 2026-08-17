from __future__ import annotations

from datetime import datetime
import logging
from pathlib import Path
import shutil
from typing import Any

import spacy
from spacy.util import is_package

from modules.mongodb_registry import MongoRegistryManager

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages the lifecycle of spaCy models with metadata persisted in MongoDB."""

    def __init__(
        self,
        models_dir: Path,
        registry: MongoRegistryManager,
    ) -> None:
        self.models_dir = models_dir
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_models: dict[str, spacy.Language] = {}
        self.registry = registry

    def _load_model_from_disk_or_package(self, model_name: str) -> spacy.Language:
        model_path = self.models_dir / model_name

        if model_path.exists():
            logger.info("Carregando modelo do disco: %s", model_path)
            return spacy.load(model_path)

        if is_package(model_name):
            logger.info("Carregando modelo do pacote instalado: %s", model_name)
            return spacy.load(model_name)

        raise ValueError(f"O modelo '{model_name}' nao foi encontrado localmente.")

    def load_model(self, model_name: str) -> spacy.Language:
        model_path = self.models_dir / model_name

        if not model_path.exists():
            if not is_package(model_name):
                logger.info("Baixando modelo %s...", model_name)
                spacy.cli.download(model_name)

            nlp = spacy.load(model_name)
            logger.info("Salvando modelo em %s...", model_path)
            nlp.to_disk(model_path)
        else:
            logger.info("Carregando modelo da pasta local %s...", model_path)
            nlp = spacy.load(model_path)

        self.loaded_models[model_name] = nlp
        self.registry.upsert_and_activate_model(model_name)
        return nlp

    def delete_model(self, model_name: str) -> None:
        model_path = self.models_dir / model_name

        deleted_from_registry = self.registry.remove_model(model_name)

        if model_path.exists():
            shutil.rmtree(model_path)

        self.loaded_models.pop(model_name, None)

        if not model_path.exists() and not deleted_from_registry:
            raise ValueError(f"O modelo '{model_name}' nao foi encontrado localmente.")

    def predict(self, text: str, model_name: str | None = None) -> dict[str, Any]:
        target_model = model_name or self.registry.get_last_used_model()

        if not target_model:
            raise ValueError("Nenhum modelo foi carregado ainda. Chame a rota /load/ primeiro.")

        if target_model not in self.loaded_models:
            self.loaded_models[target_model] = self._load_model_from_disk_or_package(target_model)

        nlp = self.loaded_models[target_model]
        doc = nlp(text)
        transaction_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        prediction_entities = {ent.label_: ent.text for ent in doc.ents}

        payload_return = {
            "input": text,
            "output": prediction_entities,
            "model_name": target_model,
            "timestamp": transaction_timestamp,
        }

        self.registry.upsert_and_activate_model(target_model)
        self.registry.save_prediction(payload_return)

        return payload_return
