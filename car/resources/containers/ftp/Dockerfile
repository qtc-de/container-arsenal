FROM alpine:3.12.0

RUN set -ex \
    && apk add vsftpd --no-cache \
    && mkdir /scripts /empty \
    && mkdir -p /ftp/anon /ftp/user

COPY config/vsftpd.conf /etc/vsftpd/
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["ash", "/scripts/start.sh"]
