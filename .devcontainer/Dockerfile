FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

ENV TZ="Asia/Taipei"

RUN apt-get update && apt-get install -y mariadb-client

WORKDIR /app

COPY ./pyproject.toml .

RUN pip install '.[dev]'