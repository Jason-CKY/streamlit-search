# FROM docker.artifact.eden.dot/infra/devops/python:3.10
FROM python:3.10

WORKDIR /code

COPY ./dev_components/openai_apiserver/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./dev_components/openai_apiserver /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]