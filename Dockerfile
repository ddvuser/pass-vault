# Dockerfile

FROM python:3

WORKDIR /app

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV COLUMNS 80

# Install system dependencies, including netcat-openbsd
RUN apt-get update \
    && apt-get install -y --no-install-recommends nano python3-pip gettext chrpath libssl-dev libxft-dev \
    libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Project dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./PassVault/ /app/

# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]
