FROM alpine:3.15.4

RUN set -ex \
    && apk --no-cache add samba  \
    && mkdir -p /scripts /config /share/public /share/private

COPY config/smb.conf /config
COPY scripts/start.sh /scripts

ENTRYPOINT ["sh", "/scripts/start.sh"]
