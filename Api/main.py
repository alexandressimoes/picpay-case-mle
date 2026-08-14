from fastapi import FastAPI

app = FastAPI()


@app.post("/load/")
async def load_model():
    """Registra um novo modelo spaCy para ser utilizado na inferência. 
    Caso o modelo já esteja registrado, ele será substituído pelo novo.
    """

    return {"message": "Novo Modelo Registrado com sucesso!"}


@app.post("/predict/")
async def predict(text: str, model_version: str = None):
    """Realiza inferência utilizando o modelo ativo ou uma versão específica.
    """
    return {"message": "Hello World"}

@app.get("/list/")
async def list_predictions():
    """Lista as predições realizadas."""
    return {"message": "Lista de predições"}



@app.get("/list-models/")
async def list_models():
    """Lista as versões de um modelo spaCy registrado."""
    return {"message": "Lista de modelos registrados"}

@app.get("/health-check/")
async def health_check():
    """Verifica a saúde do serviço."""
    return {"status": "healthy"}

@app.delete("/delete-model/")
async def delete_model(model_version: str):
    """Deleta uma versão específica de um modelo spaCy registrado."""
    return {"message": f"Modelo {model_version} deletado com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)