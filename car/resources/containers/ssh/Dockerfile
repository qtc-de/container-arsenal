FROM alpine:latest

# update the system
RUN set -ex \
    && apk --no-cache update \
    && apk --no-cache upgrade

# install ssh server and regenerate keys
RUN set -ex \
    &&  apk add openssh --no-cache\
    && rm -f /etc/ssh/ssh_host_ecdsa_key /etc/ssh/ssh_host_rsa_key \
    && ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_ecdsa_key \
    && ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key \
    && ssh-keygen -A

# add ssh user
RUN set -ex \
    && adduser --disabled-password --gecos "" default \
    && chown -R default:default /home/default

# copy configuration files into the container
RUN mkdir /scripts
COPY config/sshd_config /etc/ssh/
COPY scripts/start.sh /scripts/start.sh

# exposed resources of the container
VOLUME /home/default
EXPOSE 22/tcp

ENTRYPOINT ["ash", "/scripts/start.sh"]
