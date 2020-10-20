#!/bin/ash

set -e

if [[ -z ${LOCAL_UID} ]] || [[ ${LOCAL_UID} -eq 0 ]]; then
    LOCAL_UID=1000
fi

if ! id "default" &>/dev/null; then
    echo "[+] Creating default user..."
    adduser --disabled-password --gecos "" --shell /bin/false -u ${LOCAL_UID} default
fi

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password for user 'default': ${PASSWORD}"
fi

echo "default:${PASSWORD}" | chpasswd &> /dev/null

# The vsftpd.conf file needs to be owned by root. In order to leave volume
# permissions untouched, we create a root owned copy
echo "[+] Doing some config file magic..."
sed -e "s/<@:PORT:@>/${FTP_PORT}/" /etc/vsftpd/vsftpd.conf > /etc/vsftpd/vsftpd_active.conf
chown root:root /etc/vsftpd/vsftpd_active.conf
chmod 440 /etc/vsftpd/vsftpd_active.conf

echo "[+] Adjusting volume permissions..."
chown default:default /ftp/user /ftp/anon
chmod 750 /ftp/user
chmod 777 /ftp/anon
chmod 555 /ftp

ln -sf /proc/1/fd/1 /var/log/vsftpd.log

echo "[+] Starting vsftpd."
/usr/sbin/vsftpd /etc/vsftpd/vsftpd_active.conf
