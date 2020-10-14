FROM alpine:3.12.0

COPY scripts/add-smb-user.sh /bin/add-smb-user

RUN set -ex \
    && apk --no-cache add samba  \
    && mkdir -p /scripts /config /share/public /share/private \
    && addgroup -g 1000 default \
    && adduser -D -H -G default -s /bin/false -u 1000 default \
    && chown default:default /share/public \
    && chown default:default /share/private \
    && chmod 755 /share/private \
    && chmod 755 /share/public \
    && chmod 755 /bin/add-smb-user

COPY config/smb.conf /config
COPY scripts/start.sh /scripts

ENTRYPOINT ["sh", "/scripts/start.sh"]
