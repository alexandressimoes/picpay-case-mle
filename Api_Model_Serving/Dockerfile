FROM python:3.14

RUN mkdir /code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]