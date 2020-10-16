#!/bin/sh

set -e 

if [[ -z ${LOCAL_UID}]] || [[ ${LOCAL_UID} -eq 0 ]]; then
    LOCAL_UID=1000
fi

if ! id "default" &>/dev/null; then
    echo "[+] Creating default user..."
    adduser --disabled-password --gecos "" -u ${LOCAL_UID} default \
fi

IP=$(ip a | grep inet | grep -v 127.0.0.1 | grep -o "\([0-9]\{1,3\}\.\?\)\{4\}" | head -n 1)
echo "[+] IP address of the container: ${IP}" 

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password for user 'default': ${PASSWORD}"
fi

echo "default:${PASSWORD}" | chpasswd &>/dev/null

if [ ${ENABLE_ROOT} -eq 1 ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)
  echo "[+] Root account enabled."
  echo "[+] Generated random password for user 'root': ${PASSWORD}"
  echo "root:${PASSWORD}" | chpasswd &>/dev/null
fi

echo "[+] Adjusting volume permissions."
chown -R default:default /home/default

echo "[+] Creating login log."
echo -n "" > /tmp/logins
chmod 666 /tmp/logins
tail -f /tmp/logins &

echo "[+] Starting sshd"
/usr/sbin/sshd -D
