FROM alpine:3.14.6

RUN set -ex \
    && apk add --no-cache tftp-hpa \
    && mkdir /ftp /config
    
COPY ./config/mapfile /config/mapfile

ENTRYPOINT ["ash", "/scripts/start.sh"]
