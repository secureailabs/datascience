# syntax=docker/dockerfile:1
FROM ubuntu:18.04
RUN apt update
RUN apt install software-properties-common -y
RUN apt install python3.8 python3-pip -y
RUN mkdir /datascience
RUN apt install git -y
# RUN git clone https://$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:x-oauth-basic@github.com/secureailabs/datascience.git /datascience
# RUN python3 /datascience/datascience/build/install.py
RUN pip3 install fastapi -y
EXPOSE 8080
