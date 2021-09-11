FROM python:3.9-slim
WORKDIR /app

RUN pip install -U pip setuptools wheel
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
