FROM python:3

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# project dependencies
RUN pip install --upgrade pip
COPY ./PassVault/requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

COPY ./PassVault/ /code/

# Set the entrypoint for the container
ENTRYPOINT ["/code/entrypoint.sh"]