FROM alpine:3.15.4

RUN set -ex \
    && apk --no-cache add nginx apache2-utils shadow php8-fpm openssl \
    && mkdir -p /scripts /run/nginx/ \
    && mkdir -p /var/www/html/public \
    && mkdir -p /var/www/html/private /etc/nginx/ssl

COPY config/default.conf /etc/nginx/http.d/
COPY config/www.conf /etc/php8/php-fpm.d/
COPY config/php.ini /etc/php8/conf.d/
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["ash", "/scripts/start.sh"]
