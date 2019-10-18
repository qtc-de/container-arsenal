FROM alpine:latest

# update the system and install vsftpd
RUN set -ex \
    && apk --no-cache update \
    && apk --no-cache upgrade \
    &&  apk add vsftpd --no-cache

# add ftp user
RUN set -ex \
    && adduser --disabled-password --gecos "" default

# create required folders
RUN set -ex \
    && mkdir /scripts \
    && mkdir /empty \
    && mkdir -p /ftp/anon \
    && mkdir -p /ftp/user \
    && chown default:default /ftp/user \
    && chown default:default /ftp/anon \
    && chmod 750 /ftp/user \
    && chmod 777 /ftp/anon

# copy some files
COPY config/vsftpd.conf /etc/vsftpd/
COPY scripts/start.sh /scripts/start.sh

# exposed resources of the container
VOLUME /ftp

EXPOSE 21/tcp

ENTRYPOINT ["ash", "/scripts/start.sh"]
