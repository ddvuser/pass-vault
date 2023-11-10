FROM python:3

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV COLUMNS 80

WORKDIR /usr/src/PassVault

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends nano gettext netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Project dependencies
COPY requirements.txt /usr/src/PassVault
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the application files
COPY . /usr/src/PassVault/

# Set the entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]

