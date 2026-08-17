from fastapi import FastAPI, HTTPException
from pathlib import Path
import logging
from modules.model_manager import ModelManager
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

model_manager = ModelManager(models_dir=Path(__file__).parent / "models")
app = FastAPI()

@app.post("/load/")
async def load_model(payload: LoadModelRequest) -> LoadModelResponse:
    """
    Register a new spaCy model to be used for inference. 
    If the model is already registered, it will be replaced by the new one.
    """
    if not payload.model.strip():
        raise HTTPException(status_code=400, detail="Campo 'model' não pode ser vazio.")
    # Carrega o modelo spaCy
    await model_manager.load_model_async(payload.model)

    return LoadModelResponse(message=f"Modelo {payload.model} carregado com sucesso!\n", model=payload.model)


@app.post("/predict/", response_model=PredictResponse)
async def predict(payload: PredictRequest) -> PredictResponse:
    """
    Perform prediction inference using the active model or a specific version.
    """
    try:
        result = await model_manager.predict_async(text=payload.text, model_name=payload.model)
        return PredictResponse(message=f"Inferência realizada com sucesso. Resultado:\n {result['output']}\n", **result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Erro na inferência")
        raise HTTPException(status_code=500, detail=f"Erro na inferência: {exc}\n")


@app.get("/list/", response_model=ListPredictionsResponse)
async def list_predictions() -> ListPredictionsResponse:
    """List the predictions made."""
    predictions = await model_manager.list_predictions_async()
    return ListPredictionsResponse(predictions=predictions)


@app.get("/list-models/", response_model=ListModelsResponse)
async def list_models() -> ListModelsResponse:
    """List the downloaded spaCy models and the last used one."""
    model_registry = await model_manager.get_model_registry_async()
    return ListModelsResponse(
        downloaded_models=model_registry.get("downloaded_models", []),
        last_used_model=model_registry.get("last_used_model"),
    )

@app.get("/health-check/")
async def health_check():
    """Check the health of the service."""
    return {"status": "healthy"}

@app.delete("/delete-model/")
async def delete_model(model_version: str):
    """Deletes a specific version of a registered spaCy model."""
    try:
        await model_manager.delete_model_async(model_version)
        return {"message": f"Modelo {model_version} deletado com sucesso!"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/")
async def root():
    return {"message": "Hello World"}