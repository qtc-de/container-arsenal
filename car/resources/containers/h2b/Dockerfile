FROM alpine:3.12.0

RUN set -ex \
    && apk --no-cache add python3 py3-pip \
    && pip3 install Flask \
    && apk del py3-pip \
    && mkdir /scripts

WORKDIR /scripts
COPY scripts/h2b.py scripts/start.sh /scripts/

USER nobody
ENTRYPOINT ["sh", "/scripts/start.sh"]
