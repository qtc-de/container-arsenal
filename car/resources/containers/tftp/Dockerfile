FROM alpine:3.12.0

RUN set -ex \
    && apk add --no-cache tftp-hpa \
    && addgroup -g 1000 default \
    && adduser -D -H -G default -s /bin/false -u 1000 default \
    && mkdir /ftp /config \
    && chown default:default /ftp
    
COPY ./config/mapfile /config/mapfile

ENTRYPOINT ["ash", "/scripts/start.sh"]
