#/bin/ash

set -e 

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
