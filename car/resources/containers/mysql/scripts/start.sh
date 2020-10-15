#!/bin/sh

if [ -z ${LOCAL_UID} ]; then
    LOCAL_UID=1000
fi

echo "[+] Adjusting uid values."
usermod -u ${LOCAL_UID} mysql
groupmod -g ${LOCAL_UID} mysql
chown -R ${LOCAL_UID}:${LOCAL_UID} /var/lib/mysql

if [ "$(ls -A /var/lib/mysql)" ]; then
	echo "[+] mysql directory is already populated."
	echo "[+] Leaving users / databases and passwords untouched."
	echo "[+] Use 'car clean mysql' to start from a fresh instance."
else 

	if [ -z ${MYSQL_ROOT_PASSWORD} ]; then
	  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)
	  echo "[+] Generated random root password: ${PASSWORD}"
	  export MYSQL_ROOT_PASSWORD=${PASSWORD}
    else
      echo "[+] Specified MySQL root password:  ${MYSQL_ROOT_PASSWORD}"
    fi

	if [ -z ${MYSQL_USER} ]; then
	  echo "[+] Using following MySQL user:     default"
	  export MYSQL_USER="default"
    else
      echo "[+] Using specified MySQL user:     ${MYSQL_USER}"
    fi

	if [ -z ${MYSQL_PASSWORD} ]; then
	  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
	  echo "[+] Generated random user password: ${PASSWORD}"
	  export MYSQL_PASSWORD=${PASSWORD}
    else
      echo "[+] Specified MySQL user password:  ${MYSQL_PASSWORD}"
    fi

	if [ -z ${MYSQL_DATABASE} ]; then
	  echo "[+] Using following MySQL database: default"
	  export MYSQL_DATABASE="default"
    else
      echo "[+] Using specified MySQL database: ${MYSQL_DATABASE}"
    fi

    (sleep 20;  \
        echo "[+] Repeating MySQL credentials for easy access:"; \
        echo "[+] Root password:    $MYSQL_ROOT_PASSWORD"; \
        echo "[+] User password:    $MYSQL_PASSWORD"; \
        echo "[+] MySQL user:       $MYSQL_USER"; \
        echo "[+] MySQL database:   $MYSQL_DATABASE") &
fi

echo "[+] Starting mysql daemon"
/usr/local/bin/docker-entrypoint.sh mysqld
