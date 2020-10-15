#!/bin/sh

set -e

if [ -z ${HOST} ]; then
  echo "[-] Error. Environment variable 'HOST' needs to be set."
  echo "[-] Set the 'HOST' environment variable to the targeted AJP server."
  exit 1
fi

if [ -z ${PORT} ]; then
  echo "[-] Error. Environment variable 'PORT' needs to be set."
  echo "[-] Set the 'PORT' environment variable to the targeted port on the AJP server."
  exit 1
fi

echo "[+] Adjusting host and port values inside the jk_workes.properties file."
sed -e "s/<@:HOST:@>/${TARGET_HOST}/" /etc/apache2/jk_workers.properties | \
sed -e "s/<@:PORT:@>/${TARGET_PORT}/" > /etc/apache2/jk_workers_local.properties

echo "[+] Adjusting listening port in httpd.conf."
sed -e "s/<@:PORT:@>/${LISTEN_PORT}/" /etc/apache2/httpd_raw.conf > /etc/apache2/httpd.conf

echo "[+] Adjusting volume permissions."
chown 1000:1000 /var/log/apache2

echo "[+] Starting AJP proxy server."
httpd -DFOREGROUND
