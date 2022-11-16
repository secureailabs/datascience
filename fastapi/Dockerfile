FROM ubuntu:20.04
ENV TZ=America/Toronto
LABEL authors="adam.hall@secureailabs.com"
USER root

# Set tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update
RUN apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev git

RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"

# GIT
ARG git_personal_token
ARG branch
RUN git config --global url."https://$git_personal_token:@github.com/".insteadOf " https://github.com/"
RUN git clone -b $branch https://$git_personal_token@github.com/secureailabs/datascience.git
WORKDIR /datascience
RUN python3 build/install.py
WORKDIR /datascience/fastapi
EXPOSE 8000

# Usage
# docker build --build-arg git_personal_token={git_personal_token} --build-arg branch=BOARD-2021 -t sail/datascience-fastapi .
# docker run -it -p 8000:8000 sail/datascience-fastapi /bin/bash

# Inside container
# uvicorn main:app --host 0.0.0.0 --port 8000

