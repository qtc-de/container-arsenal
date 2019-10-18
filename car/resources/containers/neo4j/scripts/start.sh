#!/bin/bash

set -e

if [ -z ${PASSWORD} ]; then

  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password: ${PASSWORD}"

fi

echo "[+] Setting password for user 'neo4j'."
rm -f /var/lib/neo4j/data/dbms/auth
echo -n "[+] " && gosu neo4j:neo4j neo4j-admin set-initial-password ${PASSWORD}

echo "[+] Adjusting volume permissions."
chown neo4j:neo4j /data

echo "[+] Starting neo4j."
/sbin/tini -g -- /docker-entrypoint.sh neo4j
