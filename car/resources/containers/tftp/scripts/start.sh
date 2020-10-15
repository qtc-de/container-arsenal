#!/bin/ash

set -e 

echo "[+] Adjusting volume permissions."
chown default:default /ftp

echo "[+] Starting tftpd."
in.tftpd --foreground --create -m /config/mapfile --user default --secure /ftp --verbose --address "0.0.0.0:${LISTEN_PORT}"
