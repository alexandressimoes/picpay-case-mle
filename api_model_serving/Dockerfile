FROM python:3.14-slim

WORKDIR /code

COPY api_model_serving/api_requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY api_model_serving/app /code/app

WORKDIR /code/app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]