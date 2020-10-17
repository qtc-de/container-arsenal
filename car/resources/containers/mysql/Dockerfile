FROM mariadb:10.5.6

COPY scripts/start.sh /scripts/start.sh
COPY scripts/init.sql /docker-entrypoint-initdb.d/init.sql

ENTRYPOINT ["bash", "/scripts/start.sh"]
