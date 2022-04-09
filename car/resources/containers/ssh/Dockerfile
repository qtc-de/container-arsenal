FROM alpine:3.14.6

RUN set -ex \
    &&  apk add --no-cache openssh \
    && rm -f /etc/ssh/ssh_host_ecdsa_key /etc/ssh/ssh_host_rsa_key \
    && ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_ecdsa_key \
    && ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key \
    && ssh-keygen -A

COPY config/sshd_config /etc/ssh/
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["sh", "/scripts/start.sh"]
