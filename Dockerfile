FROM ubuntu:20.04
ENV TZ=America/Toronto
LABEL authors="adam.hall@secureailabs.com"
USER root

# Set tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update
RUN apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev git

# GIT
ARG git_personal_token
ARG branch
RUN git config --global url."https://$git_personal_token:@github.com/".insteadOf " https://github.com/"
RUN git clone -b $branch https://$git_personal_token@github.com/secureailabs/datascience.git
WORKDIR /datascience
RUN ls
RUN python3 build/install.py
RUN
WORKDIR /datascience/fastapi

