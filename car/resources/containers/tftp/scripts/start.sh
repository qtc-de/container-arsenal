#!/bin/ash

set -e 

if [[ -z ${LOCAL_UID} ]] || [[ ${LOCAL_UID} -eq 0 ]]; then
    LOCAL_UID=1000
fi

if ! id "default" &>/dev/null; then
    echo "[+] Creating default user..."
    adduser --disabled-password -H --gecos "" --shell /bin/false -u ${LOCAL_UID} default
fi

echo "[+] Adjusting volume permissions."
chown default:default /ftp

echo "[+] Starting syslogd."
syslogd

echo "[+] Starting TFTP server."
in.tftpd --listen --create -m /config/mapfile --user default --secure /ftp -vv --address "0.0.0.0:${LISTEN_PORT}" 

touch /var/log/messages
tail -f /var/log/messages
