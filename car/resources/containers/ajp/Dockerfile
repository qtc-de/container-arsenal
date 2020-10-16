FROM alpine:3.12.0

RUN set -ex \
    && apk add --no-cache apache2 \
    && mkdir /scripts /var/www/shm \
    && ln -s /etc/apache2 /var/www/conf

COPY config/httpd_raw.conf config/ajp.conf config/jk_workers.properties /etc/apache2/
COPY resources/mod_jk.so /usr/lib/apache2/mod_jk.so
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["sh", "/scripts/start.sh"]
