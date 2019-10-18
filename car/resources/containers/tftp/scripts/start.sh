#!/bin/ash

set -e 

echo "[+] Adjusting volume permissions."
chown default:default /ftp

echo "[+] Starting tftpd."
in.tftpd -L -c --verbose -m /config/mapfile -u default --secure /ftp
