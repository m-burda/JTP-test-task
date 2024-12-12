FROM python:3.13

WORKDIR /code

COPY ./src /code/app

ENV PYTHONPATH /code/app

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

CMD ["fastapi", "run", "app/main.py", "--port", "8080"]
