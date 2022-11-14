# pull official base image
FROM python:3.10.1-slim-buster

# LABEL org.opencontainers.image.source="https://github.com/limahuaya/tdd-docker/"

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh


# run entrypoint.sh
# https://stackoverflow.com/questions/56459461/docker-compose-exec-usr-src-app-entrypoint-sh-permission-denied
CMD ["/usr/src/app/entrypoint.sh"]

