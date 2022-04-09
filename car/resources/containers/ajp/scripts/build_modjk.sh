#!/bin/sh

echo "[+] Installing dependencies..."
    apk update
    apk add gcc
    apk add make
    apk add apache2
    apk add apr-dev
    apk add libc-dev
    apk add apache2-dev
    apk add apr-util-dev

echo "[+] Downloading mod_jk connector..."
    wget 'https://dlcdn.apache.org/tomcat/tomcat-connectors/jk/tomcat-connectors-1.2.48-src.tar.gz'
    hash=$(sha512sum tomcat-connectors-1.2.48-src.tar.gz | cut -f1 -d" ")
    if [[ "$hash" != "955a830724a3902e29032a5d2e7603d3170334e8a383d314f6bf8539d53d9f7ee4cfa0b31cfc954acb0a13d9975ed2229de085d08de3885f8679b509924fde47" ]]; then
        echo "[-] Hash Mismatch!";
        exit 1;
    fi
    tar -xvf tomcat-connectors-1.2.48-src.tar.gz

echo "[+] Building mod_jk.so..."
    cd tomcat-connectors-1.2.48-src/native
    ./configure --with-apxs="/usr/bin/apxs"
    echo '#include <sys/socket.h>' > /usr/include/sys/socketvar.h
    make

echo "[+] mod_jk.so is ready!"
