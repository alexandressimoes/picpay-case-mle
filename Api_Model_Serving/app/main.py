from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
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
def load_model(payload: LoadModelRequest) -> LoadModelResponse:
    """Registra um novo modelo spaCy para ser utilizado na inferência. 
    Caso o modelo já esteja registrado, ele será substituído pelo novo.
    """
    if not payload.model.strip():
        raise HTTPException(status_code=400, detail="Campo 'model' não pode ser vazio.")
    # Carrega o modelo spaCy
    model = model_manager.load_model(payload.model)

    return LoadModelResponse(message=f"Modelo {payload.model} carregado com sucesso!", model=payload.model)


@app.post("/predict/", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    """
    Realiza inferência utilizando o modelo ativo ou uma versão específica.
    """
    try:
        result = model_manager.predict(text=payload.text, model_name=payload.model)
        return PredictResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Erro na inferência")
        raise HTTPException(status_code=500, detail=f"Erro na inferência: {exc}")


@app.get("/list/", response_model=ListPredictionsResponse)
def list_predictions() -> ListPredictionsResponse:
    """Lista as predições realizadas."""
    if not model_manager.predictions_registry_file.exists():
        return ListPredictionsResponse(predictions=[])

    with open(model_manager.predictions_registry_file, "r", encoding="utf-8") as f:
        predictions = json.load(f)

    return ListPredictionsResponse(predictions=predictions)


@app.get("/list-models/", response_model=ListModelsResponse)
def list_models() -> ListModelsResponse:
    """Lista os modelos spaCy baixados e o último utilizado."""
    return ListModelsResponse(
        downloaded_models=model_manager.model_registry.get("downloaded_models", []),
        last_used_model=model_manager.model_registry.get("last_used_model"),
    )

@app.get("/health-check/")
def health_check():
    """Verifica a saúde do serviço."""
    return {"status": "healthy"}

@app.delete("/delete-model/")
def delete_model(model_version: str):
    """Deleta uma versão específica de um modelo spaCy registrado."""
    try:
        model_manager.delete_model(model_version)
        return {"message": f"Modelo {model_version} deletado com sucesso!"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/")
def root():
    return {"message": "Hello World"}