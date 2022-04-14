### Documentation

----

This folder contains some more detailed information on the usage and internals
of *container-arsenal*. It is not a complete documentation by now and many things
are still missing. However, you may find the information you are looking for :)


### Resource Folders

----

The *container-arsenal* documentation file in `~/.config/car/car.toml` specifies
the location of a resource folder. The default is `~/arsenal`, as you can see
in the configuration file:

```toml
[containers]
  sudo_required = true
  volume_base_path = "~/arsenal"
```

Each container from the arsenal is created with a volume mounted within the resource
folder. The *ssh* container, for example, obtains a volume mapped to `~/arsenal/ssh`.
These volumes are mapped to the *interesting* locations within the container. In case
of the *ssh* container, the volume is mapped to the home folder of the *default* user.
For the *ftp* container it is mapped to the *ftp root* and for *utils* containers like
*neo4j*, it is mapped to the database storage location.

This allows you to quickly access files that were uploaded into the containers or to
preserve the state of a database after closing and restarting a container.


### Container Access

----

If you need to troubleshoot something, it is useful to obtain a root shell within the
containers. *container-arsenal* supports the `exec` and `shell` commands to make this
quite simple:

```console
[qtc@devbox ~$] car shell ssh           # Launch a rootshell within the ssh container
[qtc@devbox ~$] car exec ssh --cmd id   # Launch the id command in the ssh container
```


### Configuration File

----

We already talked about the *container-arsenal* configuration file and its general
format:

```toml
[containers.samba]
samba_folder = "<@:BASE:@>/samba"
public_folder = "<@:BASE:@>/samba/public"
private_folder = "<@:BASE:@>/samba/private"
smb_port = "445"
```

Internally, the variable definitions from the `cat.toml` file are just included into
the `docker-compose.yml` file of the corresponding container. The `docker-compose.yml
of the **samba** container looks like this:

```yml
version: '3.7'

services:

  car.samba:
    container_name: car.samba
    image: car/samba
    build: .
    environment:
      LOCAL_UID: ${car_local_uid}
    volumes:
      - ${car_public_folder}:/share/public
      - ${car_private_folder}:/share/private
      - ./scripts/start.sh:/scripts/start.sh
      - ./config/smb.conf:/config/smb.conf
    ports:
      - "${car_smb_port}:445"
```

If you want persistent configuration changes, the `car.toml` file is the correct location
to make these. However, sometimes you want only some quick changes that only apply for
one particular situation. In this case, *mirroring* is the recommended solution. As an 
example, imagine that you need the *ssh container* that listens on port `2222` instead
of `22`.  In this case, the first step is to *mirror* the *ssh container*:

```console
[qtc@devbox ~]$ car mirror ssh
[+] Copying base folder of container ssh to current working directory.
[+] Done.
[qtc@devbox ~]$ ls -l ssh/
total 32
-rw-r--r-- 1 qtc qtc  408 Oct 17 15:31 Dockerfile
-rw-r--r-- 1 qtc qtc 4547 Oct 17 15:31 README.md
drwxr-xr-x 2 qtc qtc 4096 Oct 17 15:31 config
-rw-r--r-- 1 qtc qtc  393 Oct 17 15:48 docker-compose.yml
-rw-r--r-- 1 qtc qtc  180 Oct 17 15:31 env_info.txt
drwxr-xr-x 2 qtc qtc 4096 Oct 17 15:31 scripts
-rwxr-xr-x 1 qtc qtc  913 Oct 17 15:31 toggle-root.sh
```

As you can see, *mirroring* just copies the directory of the corresponding *docker container*
to your current working directory. Inside this directory you can find all files that were
used for the container configuration. Inside the `docker-compose.yml` file, all environment
variables that were mentioned before, are replaced by their default values. A mirrored
`docker-compose.yml` looks like this:

```yml
version: '3.7'

services:

  car.ssh:
    container_name: car.ssh
    image: car/ssh
    build: .
    environment:
      ENABLE_ROOT: 0
      LOCAL_UID: 1002
    volumes:
      - /home/qtc/arsenal/ssh:/home/default
      - ./scripts/start.sh:/scripts/start.sh
      - ./config/sshd_config:/etc/ssh/sshd_config
      - ./config/sshrc:/etc/ssh/sshrc
    ports:
      - "22:22"
```

If you now want to apply your custom port change, you can simply modify the mapping inside
the `docker-compose.yml` file and then use `car run .` from within the *mirrored* directory.

Apart from *mirroring*, you can also use environment variables to modify the container behavior.
The command `car env <container>` can be used to list available environment variables:

```console
[qtc@devbox ~]$ car env ssh
[+] Available environment variables are:
[+] Name               Current Value                   Description
[+] car_ssh_folder     /home/qtc/arsenal/ssh           SSH resource folder. Mapped as a volume into the container.
[+] car_ssh_port       22                              SSH port mapped to your local machine.
[+] car_local_uid      1000                            UID of the SSH user.
```

By setting the corresponding environment variable explicitly, you can change its default
value during container startup:

```console
[qtc@devbox ~]$ car_ssh_port=2222 car run ssh
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_ssh_folder                /home/qtc/arsenal/ssh
[+]	car_ssh_port                  2222
[+]
[+] Running: sudo -E docker-compose up
Recreating car.ssh ... done
Attaching to car.ssh
car.ssh    | [+] Creating default user...
car.ssh    | [+] IP address of the container: 172.18.0.2
car.ssh    | [+] No password was specified.
car.ssh    | [+] Generated random password for user 'default': SrAeThIp
car.ssh    | [+] Adjusting volume permissions.
car.ssh    | [+] Creating login log.
car.ssh    | [+] Starting sshd
```


### About Sudo

----

By default, *container-arsenal* uses ``sudo`` to invoke all docker relevant commands.
This is probably not required when being member of the *docker-group*. In this case,
you can apply the following setting within your ``car.toml`` configuration file:

```console
[qtc@devbox ~]$ head ~/.conf/car/car.toml
[containers]
  sudo_required = false
  [...]
```

When running with `sudo_required=true`, each *docker-command* is prefixed with
`sudo -E`. The `-E` switch for `sudo` is used to inherit all environment variables
of the parent process and is normally not recommended (as probably unwanted environment
variables are inherited too). However, in the case of *container-arsenal*, the command is
executed from within a dedicated environment, which just contains container relevant
environment variables.  Therefore, this should not be an issue.

Usage of `sudo -E` might be forbidden for users that are only able to run certain
commands with `sudo`. *container-arsenal* assumes that you are able to run `(ALL)`
commands with sudo, as in this case the following applies:

> SETENV and NOSETENV
> These tags override the value of the setenv option on a per-command basis. Note that if SETENV has been set for a command,
> the user may disable the env_reset option from the command line via the -E option. Additionally, environment variables set
> on the command line are not subject to the restrictions imposed by env_check, env_delete, or env_keep. As such, only trusted
> users should be allowed to set variables in this manner. If the command matched is ALL, the SETENV tag is implied for that command;
> this default may be overridden by use of the NOSETENV tag.

If you are only allowed to launch `docker` via `sudo`, you should think about your
configuration, as being able to run `docker` is usually almost equivalent to full *root*
access to the system ;)
