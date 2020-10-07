### mod_jk.so

----

The *ajp* container requires ``mod_jk.so`` to function correctly. Unfortunately, this *apache module* cannot be
installed by using *alpine's* package manager ``apk`` directly. Therefore, *container-arsenal* ships a precompiled
version of ``mod_jk.so`` that can be used within the container. This folder contains the scripts that were used
to build this precompiled binary.


### Building mod_jk.so

----

If you want to repeat the build process yourself, just run ``docker-compose up`` from within this directory.
The script will spin up a container based on the ``alpine:3.12.0`` image and run all required commands to
build ``mod_jk.so`` for *alpine*. The final precompiled binary can be downloaded from a *HTTP* server that
is run on the container. The corresponding link will be displayed at the end of the compilation process:

```console
[root@kali ~/mod_jk]# docker-compose up
Creating mod_jk ... done
Attaching to mod_jk
mod_jk    | [+] Installing dependencies...
mod_jk    | fetch http://dl-cdn.alpinelinux.org/alpine/v3.11/main/x86_64/APKINDEX.tar.gz
mod_jk    | fetch http://dl-cdn.alpinelinux.org/alpine/v3.11/community/x86_64/APKINDEX.tar.gz
mod_jk    | v3.11.6-149-g1ce31117c8 [http://dl-cdn.alpinelinux.org/alpine/v3.11/main]
mod_jk    | v3.11.6-151-gf905062a3f [http://dl-cdn.alpinelinux.org/alpine/v3.11/community]
mod_jk    | OK: 11277 distinct packages available
[...]
mod_jk    | [+] mod_jk.so is ready!
mod_jk    | [+] You can download it here: http://172.19.0.2/mod_jk.so
```
