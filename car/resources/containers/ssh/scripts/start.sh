#!/bin/ash

set -e 

IP=$(ip a | grep inet | grep -v 127.0.0.1 | grep -o "\([0-9]\{1,3\}\.\?\)\{4\}" | head -n 1)
echo "[+] IP address of the container: ${IP}" 

if [ -z ${PASSWORD} ]; then

  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password for user 'default': ${PASSWORD}"

fi

echo "default:${PASSWORD}" | chpasswd &>/dev/null

echo "[+] Adjusting volume permissions."
chown -R default:default /home/default


echo "[+] Starting sshd"
/usr/sbin/sshd -D
