
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt update && apt install -y g++ libpq-dev gcc musl-dev

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

COPY ./api /app/api



