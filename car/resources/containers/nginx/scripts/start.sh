#!/bin/ash

if [[ -z ${LOCAL_UID} ]] || [[ ${LOCAL_UID} -eq 0 ]]; then
    LOCAL_UID=1000
fi

echo "[+] Adjusting UID values."
usermod -u ${LOCAL_UID} nginx &> /dev/null
groupmod -g ${LOCAL_UID} nginx &> /dev/null

echo "[+] Adjusting volume permissions."
chown -R -P nginx:nginx /var/www/html

if ! [ -f /etc/nginx/ssl/webdav-cert.pem ]; then
    echo "[+] Creating TLS certificate."
    openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
        -subj "/C=ME/ST=TheShire/L=Frogmorton/O=LOTR/OU=Hobbits/CN=webdav-server" \
        -keyout /etc/nginx/ssl/webdav-key.pem  -out /etc/nginx/ssl/webdav-cert.pem &> /dev/null
fi

if [ -z ${PASSWORD} ]; then
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  echo "[+] No password was specified."
  echo "[+] Generated random password: ${PASSWORD}"
fi

echo "[+] Creating .htpasswd file."
echo "[+] WebDAV access allowed for default:${PASSWORD}"
htpasswd -b -c /etc/nginx/http.d/.htpasswd default ${PASSWORD} &> /dev/null

echo "[+] Starting nginx daemon."
/usr/sbin/nginx -g "daemon off;"
