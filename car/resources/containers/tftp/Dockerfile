FROM alpine:latest

# update the system and install vsftpd
RUN set -ex \
    && apk --no-cache update \
    && apk --no-cache upgrade \
    && apk add --no-cache tftp-hpa

# create ftp user
RUN set -ex \
    && addgroup -g 1000 default \
    && adduser -S -D -H -u 1000 default

# create ftp and config directory
RUN set -ex \
    && mkdir /ftp \
    && mkdir /config \
    && chown default:default /ftp
    
# copy mapfile for easiert support of windows clients
COPY ./config/mapfile /config/mapfile

# exposed resources of the container
VOLUME /ftp
EXPOSE 69/udp

ENTRYPOINT ["ash", "/scripts/start.sh"]
