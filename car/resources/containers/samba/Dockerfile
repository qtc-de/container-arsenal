FROM alpine:latest

# update the system and add the required packages
RUN set -ex \
    && apk --no-cache update \
    && apk --no-cache upgrade \
    && apk --no-cache add samba samba-common-tools supervisor

# create folders for configuration, script and share files
RUN set -ex \
    && mkdir /config \
    && mkdir /scripts \
    && mkdir -p /share/public \
    && mkdir -p /share/private

# add a non-root user and group as a default user for smb access
RUN set -ex \
    && addgroup -g 1000 default \
    && adduser -D -H -G default -s /bin/false -u 1000 default

# Make the shared folders writable
RUN set -ex \
    && chown default:default /share/public \
    && chown default:default /share/private \
    && chmod 775 /share/private \
    && chmod 775 /share/public

# copy configuration files into the container
COPY config/supervisord.conf /config/
COPY config/smb.conf /config/
COPY scripts/add-smb-user.sh /scripts
COPY scripts/start.sh /scripts

# generate symbolic links for the copied scripts
RUN set -ex \
    && chmod 755 /scripts/add-smb-user.sh \
    && ln -s /scripts/add-smb-user.sh /bin/add-smb-user

# exposed resources of the container
VOLUME /config /share
EXPOSE 135/tcp 137/udp 138/udp 139/tcp 445/tcp

ENTRYPOINT ["ash", "/scripts/start.sh"]
