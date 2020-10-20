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

echo "[+] Starting tftpd."
in.tftpd --listen --create -m /config/mapfile --user default --secure /ftp --verbose --address "0.0.0.0:${LISTEN_PORT}" 

LIST_CMD='find /ftp -type f | xargs ls -ld'
echo "[+] Current server contents:"
eval $LIST_CMD | tee /tmp/files_old

echo "[+] New uploaded files:"
while true; do
    sleep 5
    eval $LIST_CMD > /tmp/files_new
    diff /tmp/files_old /tmp/files_new | grep -E "^\+[^+]" | cut -f2 -d"+"
    cp /tmp/files_new /tmp/files_old
done
