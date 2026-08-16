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
    """Registra um novo modelo spaCy para ser utilizado na inferência. 
    Caso o modelo já esteja registrado, ele será substituído pelo novo.
    """
    if not payload.model.strip():
        raise HTTPException(status_code=400, detail="Campo 'model' não pode ser vazio.")
    # Carrega o modelo spaCy
    await model_manager.load_model_async(payload.model)

    return LoadModelResponse(message=f"Modelo {payload.model} carregado com sucesso!", model=payload.model)


@app.post("/predict/", response_model=PredictResponse)
async def predict(payload: PredictRequest) -> PredictResponse:
    """
    Realiza inferência utilizando o modelo ativo ou uma versão específica.
    """
    try:
        result = await model_manager.predict_async(text=payload.text, model_name=payload.model)
        return PredictResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Erro na inferência")
        raise HTTPException(status_code=500, detail=f"Erro na inferência: {exc}")


@app.get("/list/", response_model=ListPredictionsResponse)
async def list_predictions() -> ListPredictionsResponse:
    """Lista as predições realizadas."""
    predictions = await model_manager.list_predictions_async()
    return ListPredictionsResponse(predictions=predictions)


@app.get("/list-models/", response_model=ListModelsResponse)
async def list_models() -> ListModelsResponse:
    """Lista os modelos spaCy baixados e o último utilizado."""
    model_registry = await model_manager.get_model_registry_async()
    return ListModelsResponse(
        downloaded_models=model_registry.get("downloaded_models", []),
        last_used_model=model_registry.get("last_used_model"),
    )

@app.get("/health-check/")
async def health_check():
    """Verifica a saúde do serviço."""
    return {"status": "healthy"}

@app.delete("/delete-model/")
async def delete_model(model_version: str):
    """Deleta uma versão específica de um modelo spaCy registrado."""
    try:
        await model_manager.delete_model_async(model_version)
        return {"message": f"Modelo {model_version} deletado com sucesso!"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/")
async def root():
    return {"message": "Hello World"}