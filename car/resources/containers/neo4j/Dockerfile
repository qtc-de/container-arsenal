FROM neo4j:latest

RUN set -ex \
    && mkdir /scripts \
    && usermod -u 1000 neo4j \
    && groupmod -g 1000 neo4j \
    && chown 1000:1000 /data

COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["bash", "/scripts/start.sh"]
