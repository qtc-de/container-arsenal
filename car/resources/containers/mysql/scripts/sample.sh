#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "$0 <IP>"
    exit 1
fi

HOST=$1

echo -n "Password: "
read -s PASS
echo ""

read -r -d '' SQL <<'EOF'
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) DEFAULT CHARSET=utf8;

INSERT INTO `users` (`username`, `email`, `password`) VALUES
  ('admin', 'admin@container-arsenal.de', SHA1('password')),
  ('user', 'user@container-arsenal.de', SHA1('secure')),
  ('bob', 'bob@bobbobbobbob.bob', SHA1('bob'));
EOF

mysql -u root -h $HOST --password="$PASS" -e "$SQL" default
mysql -u root -h $HOST --password="$PASS" -e "select * from users;" default
