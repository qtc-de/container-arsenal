#!/bin/bash

SSH_CONFIG="./config/sshd_config"
COMPOSE_FILE="./docker-compose.yml"

if [ "$(head -n1 config/sshd_config)" == "AllowUsers default" ]; then
    echo "[+] Enabling root login..."
    sed -i 's/AllowUsers default/AllowUsers default root/' $SSH_CONFIG
    sed -i 's/PermitRootLogin no/PermitRootLogin yes/' $SSH_CONFIG
    sed -i 's/ENABLE_ROOT: 0/ENABLE_ROOT: 1/' $COMPOSE_FILE
    echo "[+] root login enabled."
elif [ "$(head -n1 config/sshd_config)" == "AllowUsers default root" ]; then 
    echo "[+] Disabling root login..."
    sed -i 's/AllowUsers default root/AllowUsers default/' $SSH_CONFIG
    sed -i 's/PermitRootLogin yes/PermitRootLogin no/' $SSH_CONFIG
    sed -i 's/ENABLE_ROOT: 1/ENABLE_ROOT: 0/' $COMPOSE_FILE
    echo "[+] root login disabled."
else
    echo "[+] '$SSH_CONFIG' starts with unenxpected line."
    echo "[+] Have you modified it manually?"
    echo "[+] Aborted."
fi
