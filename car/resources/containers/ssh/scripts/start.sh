#!/bin/sh

set -e

FRESH="/root/.started_before"
LOGFILE="/var/log/ssh_logins.log"

IP=$(ip a | grep inet | grep -v 127.0.0.1 | grep -o "\([0-9]\{1,3\}\.\?\)\{4\}" | head -n 1)
echo "[+] IP address of the container: ${IP}"

if ! [[ -f ${FRESH} ]]; then
    echo "[+] Regenerating SSH keys."
    rm -f /etc/ssh/ssh_host_*
    ssh-keygen -A
    touch ${FRESH}
fi

if [[ -z ${LOCAL_UID} ]] || [[ ${LOCAL_UID} -eq 0 ]]; then
    LOCAL_UID=1000
fi

if ! id "default" &>/dev/null; then
    echo "[+] Creating default user..."
    adduser --disabled-password -s /usr/bin/rssh --gecos "" -u ${LOCAL_UID} default
fi

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

echo "[+] Creating login log."
echo -n > ${LOGFILE}
chmod 622 ${LOGFILE}
tail -f ${LOGFILE} &

echo "[+] Generating SSH key."
rm -rf /home/default/.ssh
mkdir /home/default/.ssh
ssh-keygen -t ed25519 -f /home/default/.ssh/key -q -N ""
mv /home/default/.ssh/key.pub /home/default/.ssh/authorized_keys

echo "[+] Adjusting volume permissions."
chown -R -P default:default /home/default

echo "[+] SSH private key for user default:"
cat /home/default/.ssh/key

echo "[+] Starting sshd"
/usr/sbin/sshd -D
