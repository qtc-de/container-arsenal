#!/bin/bash

set -e

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password: ${PASSWORD}"
fi


if [ -f /var/lib/neo4j/data/dbms/started_before ]; then

	echo -e "[+] neo4j was started before.\n[+] Password is altered in the database..."
	sed -i -e 's/#dbms.security.auth_enabled=false/dbms.security.auth_enabled=false/' /var/lib/neo4j/conf/neo4j.conf

	echo "[+]    Starting 'neo4j'..."
	gosu neo4j:neo4j bin/neo4j start &> /dev/null

	set +e
	WGET_STATUS=1
	while [ $WGET_STATUS -ne 0 ]; do
		sleep 0.25
		wget http://localhost:7474/ -t 1 &> /dev/null
		WGET_STATUS=$?
	done
	set -e
	rm index.html

	echo "[+]    Changing password..."
	echo "DROP USER neo4j;" | bin/cypher-shell -d system
	echo "CREATE USER neo4j SET PASSWORD '${PASSWORD}' CHANGE NOT REQUIRED;" | bin/cypher-shell -d system

	echo "[+]    Stopping 'neo4j'..."
	gosu neo4j:neo4j bin/neo4j stop &> /dev/null
	sed -i -e 's/dbms.security.auth_enabled=false/#dbms.security.auth_enabled=false/' /var/lib/neo4j/conf/neo4j.conf

else
    # For the mysql container this is done in the docker file. However, for neo4j this causes
    # the corresponding docker-layer to be of ~100MB size. Therefore, it is done in the startup
    # script.
    usermod -u 1000 neo4j &> /dev/null
    groupmod -g 1000 neo4j &> /dev/null
    chown -R neo4j:neo4j /data
	echo "[+] Setting password for user 'neo4j'."
	rm -f /var/lib/neo4j/data/dbms/auth /var/lib/neo4j/data/dbms/auth.ini
	echo -n "[+] " && gosu neo4j:neo4j neo4j-admin set-initial-password ${PASSWORD}
	touch /var/lib/neo4j/data/dbms/started_before
fi

echo "[+] Adjusting volume permissions."
chown -R neo4j:neo4j /data

echo "[+] Starting neo4j."
/docker-entrypoint.sh neo4j console
