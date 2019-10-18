#!/bin/bash

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

echo "[+] Adjusting host and port values inside the jk_workes properties file"
cp /usr/local/apache2/conf/extra/jk_workers.properties /usr/local/apache2/conf/extra/jk_workers_local.properties
sed -i -e "s/<@:HOST:@>/${HOST}/" /usr/local/apache2/conf/extra/jk_workers_local.properties
sed -i -e "s/<@:PORT:@>/${PORT}/" /usr/local/apache2/conf/extra/jk_workers_local.properties

echo "[+] Adjusting volume permissions."
chown 1000:1000 /usr/local/apache2/logs

echo "[+] Starting AJP proxy server."
httpd-foreground
