#!/bin/ash

set -e

if [ -z ${PASSWORD} ]; then

  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password for user 'default': ${PASSWORD}"

fi

echo "default:${PASSWORD}" | chpasswd &> /dev/null

# The vsftpd.conf file needs to be owned by root. In order to leave volume
# permissions untouched, we create a root owned copy
echo "[+] Doing some config file magic."
cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd_active.conf
chown root:root /etc/vsftpd/vsftpd_active.conf
chmod 440 /etc/vsftpd/vsftpd_active.conf

# Make sure that volumes have the correct permissions
echo "[+] Adjustign volume permissions"
chown default:default /ftp/user
chown default:default /ftp/anon
chmod 750 /ftp/user
chmod 777 /ftp/anon

echo "[+] Starting vsftpd."
/usr/sbin/vsftpd /etc/vsftpd/vsftpd_active.conf
