#!/bin/ash

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password for user 'default': ${PASSWORD}"
fi

echo -e "${PASSWORD}\n${PASSWORD}" | smbpasswd -a -s -c /config/smb.conf default &> /dev/null

echo "[+] Adjusting volume permissions."
chown default:default /share/public
chown default:default /share/private
chmod 775 /share/private
chmod 775 /share/public

# If we need additional users with fixed passwords we can use the following command:
#add-smb-user "user" "password"

echo "[+] Starting samba service."
smbd --foreground --no-process-group --log-stdout --configfile /config/smb.conf
