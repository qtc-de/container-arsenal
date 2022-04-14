FROM mariadb:10.7.3

COPY scripts/start.sh /scripts/start.sh
COPY scripts/init.sql /docker-entrypoint-initdb.d/init.sql

ENTRYPOINT ["bash", "/scripts/start.sh"]
