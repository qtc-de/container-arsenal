###########################################
###             Build Stage             ###
###########################################
FROM alpine:3.12.0 AS builder
COPY scripts/build_modjk.sh /build/build.sh
WORKDIR /build
RUN ./build.sh

###########################################
###          Container Stage            ###
###########################################
FROM alpine:3.12.0

RUN set -ex \
    && apk add --no-cache apache2 \
    && mkdir /scripts /var/www/shm \
    && ln -s /etc/apache2 /var/www/conf

COPY config/httpd_raw.conf config/ajp.conf config/jk_workers.properties /etc/apache2/
COPY scripts/start.sh /scripts/start.sh

COPY --from=builder /build/tomcat-connectors-1.2.48-src/native/apache-2.0/mod_jk.so /usr/lib/apache2/mod_jk.so

ENTRYPOINT ["sh", "/scripts/start.sh"]
