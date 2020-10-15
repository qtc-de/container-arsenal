FROM alpine:3.12.0

RUN set -ex \
    && apk --no-cache add python3 py3-pip su-exec \
    && pip3 install Flask \
    && apk del py3-pip \
    && mkdir /scripts

WORKDIR /scripts
COPY scripts/h2b.py /scripts/
COPY scripts/start.sh /scripts/

ENTRYPOINT ["sh", "/scripts/start.sh"]
