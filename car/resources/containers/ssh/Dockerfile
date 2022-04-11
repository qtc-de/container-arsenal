FROM alpine:3.15.4

RUN set -ex \
    &&  apk add --no-cache openssh rssh \
    && rm -f /etc/ssh/ssh_host_* \
    && ssh-keygen -A

COPY config/sshd_config config/sshrc /etc/ssh/
COPY config/rssh.conf /etc/
COPY scripts/start.sh /scripts/start.sh

ENTRYPOINT ["sh", "/scripts/start.sh"]
