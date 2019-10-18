#!/bin/ash

if [ $# -ne 2 ]; then
	echo "$0 <USERNAME> <PASSWORD>"
	exit 1
fi

set -ex

addgroup $1
adduser -D -H -G $1 -s /bin/false $1
echo -e "$2\n$2" | smbpasswd -a -s -c /config/smb.conf $1
