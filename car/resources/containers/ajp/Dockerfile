FROM httpd:latest

RUN set -ex \
    && apt update \
    && apt -y install libapache2-mod-jk \
    && apt clean

RUN set -ex \
    && mkdir /scripts \
    && chown 1000:1000 /usr/local/apache2/logs

COPY config/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY config/ajp.conf /usr/local/apache2/conf/extra/ajp.conf
COPY config/jk_workers.properties /usr/local/apache2/conf/extra/jk_workers.properties
COPY scripts/start.sh /scripts/start.sh


ENTRYPOINT ["bash", "/scripts/start.sh"]
