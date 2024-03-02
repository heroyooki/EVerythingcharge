FROM python:3.11.3-slim-bullseye

RUN apt-get update

RUN mkdir -p /usr/src/ocpp/api
RUN mkdir -p /usr/src/ocpp/worker

RUN mkdir -p /usr/src/ocpp/frontend

WORKDIR /usr/src/ocpp

COPY backend /usr/src/ocpp/api
COPY backend/worker /usr/src/ocpp/worker

COPY frontend /usr/src/ocpp/frontend

ENV PYTHONPATH="/usr/src/ocpp/api:/usr/src/ocpp/worker"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -r api/requirements.txt --upgrade pip

CMD ["python", "/usr/src/ocpp/worker/main.py"]
