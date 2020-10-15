FROM alpine:3.12.0

RUN set -ex \
    && apk add --no-cache apache2 \
    && mkdir /scripts /var/www/shm \
    && chown 1000:1000 /var/log/apache2 \
    && ln -s /etc/apache2 /var/www/conf

COPY config/httpd.conf /etc/apache2/httpd_raw.conf
COPY config/ajp.conf /etc/apache2/ajp.conf
COPY config/jk_workers.properties /etc/apache2/jk_workers.properties

COPY resources/mod_jk.so /usr/lib/apache2/mod_jk.so
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["sh", "/scripts/start.sh"]
