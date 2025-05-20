# syntax=docker/dockerfile:1.4

########################################################
# phase1: install python requirements
########################################################
FROM python:3.11-slim AS builder
LABEL authors="jamesyeh"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=DjangoProject.settings

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

########################################################
# phase2: working environment
########################################################
FROM python:3.11-slim

LABEL authors="jamesyeh"

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=DjangoProject.settings

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8080 \
    "]