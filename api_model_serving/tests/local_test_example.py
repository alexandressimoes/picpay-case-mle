from app.modules.model_manager import ModelManager
from pathlib import Path
model_path = Path(Path(__file__).parent / "app/models")
model_manager = ModelManager(models_dir=model_path)


import requests

r = requests.post("http://localhost:8000/load/",
                  json={"model": "en_core_web_sm"})

r = requests.post("http://localhost:8000/predict/",
                  json={"text": "Apple announced a new product in California costing 1000 dollars.",
                        "model": "en_core_web_sm"})

print(r.status_code)  # 200
print(r.json())    