#!/bin/ash

if [[ -z ${LOCAL_UID} ]] || [[ ${LOCAL_UID} -eq 0 ]]; then
    LOCAL_UID=1000
fi

if ! id "default" &>/dev/null; then
    echo "[+] Creating default user..."
    adduser --disabled-password -H --gecos "" --shell /bin/false -u ${LOCAL_UID} default
fi

echo "[+] Adjusting volume permissions..."
chown default:default /share/public /share/private
chmod 775 /share/private /share/public

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password for user 'default': ${PASSWORD}"
fi

echo -e "${PASSWORD}\n${PASSWORD}" | smbpasswd -a -s -c /config/smb.conf default &> /dev/null

echo "[+] Starting samba service."
smbd --foreground --no-process-group --log-stdout --configfile /config/smb.conf
