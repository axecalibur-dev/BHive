# Use Python 3.11 as the base image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /app

ENV DOCKER_PORT=8000

EXPOSE 8000
