FROM alpine:3.15.4

RUN set -ex \
    && apk --no-cache add nginx apache2-utils shadow openssl \
    && mkdir -p /scripts /run/nginx/ \
    && mkdir -p /var/www/html/download \
    && mkdir -p /var/www/html/upload /etc/nginx/ssl

COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["ash", "/scripts/start.sh"]
