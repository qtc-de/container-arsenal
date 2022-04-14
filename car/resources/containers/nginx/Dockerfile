FROM alpine:3.15.4

RUN set -ex \
    && apk --no-cache add nginx apache2-utils shadow \
    && mkdir -p /scripts /run/nginx/ \
    && mkdir -p /var/www/html/download \
    && mkdir -p /var/www/html/upload

COPY scripts/start.sh /scripts/start.sh
COPY ssl /etc/nginx/ssl

ENTRYPOINT ["ash", "/scripts/start.sh"]
