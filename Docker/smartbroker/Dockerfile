FROM ubuntu:20.04
ENV TZ=America/Toronto
LABEL authors="adam.hall@secureailabs.com"
USER root

# Set tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  nginx \
  wget \
  curl \
  sudo \
  build-essential \
  python3-pip \
  iputils-ping

RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY nginx.conf /etc/nginx/nginx.conf

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

ENTRYPOINT [ "/Entrypoint.sh" ]
