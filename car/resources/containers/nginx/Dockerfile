FROM alpine:3.12.0

RUN set -ex \
    && apk --no-cache add nginx \
    && apk --no-cache add apache2-utils \
    && mkdir /scripts /run/nginx/ \
    && mkdir -p /var/www/html/download \
    && mkdir -p /var/www/html/upload \
    && chown 1000:1000 /var/www/html/download \
    && chown 1000:nginx /var/www/html/upload \
    && chmod 775 /var/www/html/upload

COPY scripts/start.sh /scripts/start.sh
COPY ssl /etc/nginx/ssl

ENTRYPOINT ["ash", "/scripts/start.sh"]
