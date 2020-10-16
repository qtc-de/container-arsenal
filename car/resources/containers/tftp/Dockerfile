FROM alpine:3.12.0

RUN set -ex \
    && apk add --no-cache tftp-hpa \
    && mkdir /ftp /config
    
COPY ./config/mapfile /config/mapfile

ENTRYPOINT ["ash", "/scripts/start.sh"]
