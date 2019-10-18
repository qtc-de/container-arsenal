#!/bin/ash

if [ -z ${PASSWORD} ]; then

  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password: ${PASSWORD}"

fi

echo "[+] Creating .htpasswd file"
htpasswd -b -c /etc/nginx/conf.d/.htpasswd default ${PASSWORD} &> /dev/null

echo "[+] Adjusting volume permissions."
chown 1000:1000 /var/www/html/download
chown 1000:nginx /var/www/html/upload
chmod 775 /var/www/html/upload

echo "[+] Starting nginx daemon"
/usr/sbin/nginx -g "daemon off;"
