FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get -y install \
    python3 \
    python3-dev \
    python3-pip \
 && rm -rf /var/cache/apt/*

## Python packages
COPY docker/requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt \
 && rm -rf /root/.cache/pip

COPY bin /opt

WORKDIR /opt
