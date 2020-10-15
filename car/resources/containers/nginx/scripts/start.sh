#!/bin/ash

if [ -z ${LOCAL_UID} ]; then
    LOCAL_UID=1000
fi

echo "[+] Adjusting UID values."
usermod -u ${LOCAL_UID} nginx &> /dev/null
groupmod -g ${LOCAL_UID} nginx &> /dev/null
chown nginx:nginx /var/www/html/download
chown nginx:nginx /var/www/html/upload

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password: ${PASSWORD}"
fi

echo "[+] Creating .htpasswd file."
echo "[+] WebDAV access allowed for default:${PASSWORD}"
htpasswd -b -c /etc/nginx/conf.d/.htpasswd default ${PASSWORD} &> /dev/null

echo "[+] Starting nginx daemon."
/usr/sbin/nginx -g "daemon off;"
