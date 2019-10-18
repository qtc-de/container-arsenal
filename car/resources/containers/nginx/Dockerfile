FROM nginx:alpine

RUN set -ex \
    && apk --no-cache update \
    && apk add apache2-utils --no-cache

RUN set -ex \
    && mkdir /scripts \
    && mkdir -p /var/www/html/download \
    && mkdir -p /var/www/html/upload \
    && chown 1000:1000 /var/www/html/download \
    && chown 1000:nginx /var/www/html/upload \
    && chmod 775 /var/www/html/upload

COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["ash", "/scripts/start.sh"]
