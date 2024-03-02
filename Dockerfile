FROM python:3.11.3-slim-bullseye

RUN apt-get update

RUN mkdir -p /ocpp/api
RUN mkdir -p /ocpp/worker

RUN mkdir -p /ocpp/frontend

WORKDIR /ocpp/api

COPY backend /ocpp/api
COPY backend/worker /ocpp/worker

COPY frontend /ocpp/frontend

ENV PYTHONPATH="/ocpp/api:/ocpp/worker"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt --upgrade pip

CMD ["python", "/ocpp/worker/main.py"]
