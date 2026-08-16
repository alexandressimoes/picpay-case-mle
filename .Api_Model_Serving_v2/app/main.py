from __future__ import annotations

import logging
import os

from fastapi import FastAPI, HTTPException
from pathlib import Path

from modules.model_manager import ModelManager
from modules.mongodb_registry import MongoRegistryManager
from schemas.schemas import (
    LoadModelRequest,
    LoadModelResponse,
    PredictRequest,
    PredictResponse,
    ListPredictionsResponse,
    ListModelsResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://admin:admin1234@mongodb:27017/picpay_metadata?authSource=admin")
MONGODB_DB = os.getenv("MONGODB_DB", "picpay_metadata")
MONGODB_MODELS_COLLECTION = os.getenv("MONGODB_MODELS_COLLECTION", "model_registry")
MONGODB_TRANSACTIONS_COLLECTION = os.getenv("MONGODB_TRANSACTIONS_COLLECTION", "transactions_registry")

registry = MongoRegistryManager(
    mongodb_uri=MONGODB_URI,
    db_name=MONGODB_DB,
    models_collection=MONGODB_MODELS_COLLECTION,
    transactions_collection=MONGODB_TRANSACTIONS_COLLECTION,
)
model_manager = ModelManager(models_dir=Path(__file__).parent / "models", registry=registry)
app = FastAPI(title="Model Serving API")


@app.post("/load/")
def load_model(payload: LoadModelRequest) -> LoadModelResponse:
    if not payload.model.strip():
        raise HTTPException(status_code=400, detail="Campo 'model' nao pode ser vazio.")

    try:
        model_manager.load_model(payload.model)
        return LoadModelResponse(message=f"Modelo {payload.model} carregado com sucesso!", model=payload.model)
    except Exception as exc:
        logger.exception("Erro ao carregar modelo")
        raise HTTPException(status_code=500, detail=f"Erro ao carregar modelo: {exc}")


@app.post("/predict/", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    try:
        result = model_manager.predict(text=payload.text, model_name=payload.model)
        return PredictResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Erro na inferencia")
        raise HTTPException(status_code=500, detail=f"Erro na inferencia: {exc}")


@app.get("/list/", response_model=ListPredictionsResponse)
def list_predictions() -> ListPredictionsResponse:
    return ListPredictionsResponse(predictions=registry.list_predictions())


@app.get("/list-models/", response_model=ListModelsResponse)
def list_models() -> ListModelsResponse:
    model_registry = registry.get_model_registry()
    return ListModelsResponse(
        downloaded_models=model_registry.get("downloaded_models", []),
        last_used_model=model_registry.get("last_used_model"),
    )


@app.get("/health-check/")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready/")
def readiness() -> dict[str, str]:
    if not registry.ping():
        raise HTTPException(status_code=503, detail="MongoDB indisponivel")
    return {"status": "ready"}


@app.delete("/delete-model/")
def delete_model(model_version: str) -> dict[str, str]:
    try:
        model_manager.delete_model(model_version)
        return {"message": f"Modelo {model_version} deletado com sucesso!"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}