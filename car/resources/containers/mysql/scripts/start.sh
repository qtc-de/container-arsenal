#!/bin/sh

if [ "$(ls -A /var/lib/mysql)" ]; then
	echo "[+] mysql directory is already populated."
	echo "[+] Leaving users / databases and passwords untouched."
	echo "[+] Use 'car clean mysql' to start from a fresh instance."
else 

	if [ -z ${MYSQL_ROOT_PASSWORD} ]; then
	  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)
	  echo "[+] No root password was specified."
	  echo "[+] Generated random root password: ${PASSWORD}"
	  export MYSQL_ROOT_PASSWORD=${PASSWORD}
	fi

	if [ -z ${MYSQL_USER} ]; then
	  echo "[+] No database user specified."
	  echo "[+] Database user 'default' will be created."
	  export MYSQL_USER="default"
	fi

	if [ -z ${MYSQL_PASSWORD} ]; then
	  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
	  echo "[+] No user password was specified."
	  echo "[+] Generated random user password: ${PASSWORD}"
	  export MYSQL_PASSWORD=${PASSWORD}
	fi

	if [ -z ${MYSQL_DATABASE} ]; then
	  echo "[+] No database name specified."
	  echo "[+] Database 'default' will be created."
	  export MYSQL_DATABASE="default"
	fi
fi

echo "[+] Adjusting volume permissions."
chown 1000:1000 /var/lib/mysql

echo "[+] Starting mysql daemon"
/usr/local/bin/docker-entrypoint.sh mysqld
