FROM ubuntu:22.04

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    gcc \
    curl \
    gpg-agent \
    apt-utils \
    apt-transport-https \
    git \
    python3-dev \
    python3-pip \ 
    acl \
    sssd \
    xterm


RUN git clone https://gitlab.com/DrWhatson/astro-cutouts.git && \
    cd astro-cutouts && \
    pip3 install -r requirements_spefic.txt .

RUN mkdir /examples
RUN mkdir /scripts

COPY examples /examples
COPY scripts /scripts

ADD nsswitch.conf /etc/

WORKDIR /scripts

ENTRYPOINT ["./pipeline.sh"]
