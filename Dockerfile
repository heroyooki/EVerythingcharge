FROM python:3.11.3-slim-bullseye

RUN apt-get update

RUN mkdir -p /ocpp/backend
RUN mkdir -p /ocpp/frontend

WORKDIR /ocpp/backend

COPY backend /ocpp/backend
COPY frontend /ocpp/frontend

ENV PYTHONPATH="/ocpp/backend"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt --upgrade pip

CMD ["python", "/ocpp/backend/worker/main.py"]
