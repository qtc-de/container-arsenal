FROM alpine:3.12.0

RUN set -ex \
    && addgroup -g 1000 nginx \
    && adduser -D -H -G nginx -s /bin/false -u 1000 nginx \
    && apk --no-cache add nginx apache2-utils \
    && mkdir /scripts /run/nginx/ \
    && mkdir -p /var/www/html/download \
    && mkdir -p /var/www/html/upload \
    && chown 1000:1000 /var/www/html/download \
    && chown 1000:1000 /var/www/html/upload

COPY scripts/start.sh /scripts/start.sh
COPY ssl /etc/nginx/ssl

ENTRYPOINT ["ash", "/scripts/start.sh"]
