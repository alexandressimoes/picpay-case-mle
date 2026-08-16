from app.modules.model_manager import ModelManager
from pathlib import Path
model_path = Path(Path(__file__).parent / "app/models")
model_manager = ModelManager(models_dir=model_path)

import asyncio

nlp = model_manager.load_model("en_core_web_sm")

texto = "pay "

prediction = model_manager.predict(text=texto, model_name="en_core_web_sm")
print(prediction)



prediction = nlp(texto)
for token in prediction:
    print(f"Token.text: {token.text}, ",
          f"Token.lemma_: {token.lemma_}, ",
          f"Token.pos_: {token.pos_}, ",
          f"Token.tag_: {token.tag_}, ",
          f"Token.dep_: {token.dep_}, ",
          f"Token.shape_: {token.shape_}, ",
          f"Token.is_alpha: {token.is_alpha}, ",
          f"Token.is_stop: {token.is_stop}")