FROM mariadb:10.5.6

RUN set -ex \
    && mkdir /scripts \
    && usermod -u 1000 mysql \
    && groupmod -g 1000 mysql \
    && chown 1000:1000 /var/lib/mysql

COPY scripts/start.sh /scripts/start.sh
COPY scripts/init.sql /docker-entrypoint-initdb.d/init.sql

ENTRYPOINT ["bash", "/scripts/start.sh"]
