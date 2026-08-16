FROM python:3.14-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY Api_Model_Serving_v2/app /code/app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]