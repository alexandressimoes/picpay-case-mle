from pydantic import BaseModel, Field
from typing import List, Dict, Any

class LoadModelRequest(BaseModel):
    model: str = Field(..., description="Nome do modelo spaCy, ex: en_core_web_sm")


class LoadModelResponse(BaseModel):
    message: str
    model: str

class PredictRequest(BaseModel):
    text: str = Field(..., description="Texto para inferência")
    model: str | None = Field(None, description="Modelo spaCy a ser utilizado para inferência. Se não fornecido, o último modelo carregado será usado.")


class PredictResponse(BaseModel):
    input: str
    output: Dict[str, str]
    model_name: str
    timestamp: str


class ListPredictionsResponse(BaseModel):
    predictions: List[PredictResponse]


class ListModelsResponse(BaseModel):
    downloaded_models: List[str]
    last_used_model: str | None