FROM alpine:3.12.0

RUN set -ex \
    && apk add vsftpd --no-cache \
    && adduser --disabled-password --gecos "" --shell /bin/false default \
    && mkdir /scripts /empty \
    && mkdir -p /ftp/anon /ftp/user \
    && chown default:default /ftp/anon /ftp/user \
    && chmod 750 /ftp/user \
    && chmod 777 /ftp/anon \
    && chmod 555 /ftp

COPY config/vsftpd.conf /etc/vsftpd/
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["ash", "/scripts/start.sh"]
