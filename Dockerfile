FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


WORKDIR /app
COPY ./django-app /app/

RUN apt-get update && apt-get install -y build-essential libpq-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

