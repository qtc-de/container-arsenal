FROM python:3.7-slim

RUN set -ex \
    && apt clean \
    && apt -y update
    
RUN set -ex \
    && apt -y install python3-dev \
    && apt -y install build-essential \
    && pip3 install Flask \
    && apt clean

RUN mkdir /scripts
RUN mkdir /dummy
WORKDIR /scripts

COPY scripts/h2b.py /scripts/
COPY scripts/start.sh /scripts/

ENTRYPOINT ["bash", "/scripts/start.sh"]
