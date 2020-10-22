## SSH

----

This container starts an *alpine based ssh server* with a single allowed user account (username: ``default``). 
The password for the user account is generated randomly during container startup and is displayed
in the launching terminal. The *home folder* of the user ``default`` is mapped to the top level resource
folder of the container as a *docker volume*.

By default, the *sshd_config* has *root login* disabled and only allows *ssh access* for the user ``default``. You
can enable *root access* as described in the section [enabling root login](#enabling-root-login). However,
notice that this has some security implications.

Port forwarding and tunneling is allowed by the *sshd_config*. The main benefit of this container is that
*ssh* can be used for port forwarding, file transfers and network tunnels.


### Example Usage

----

First of all, we start the *ssh* container on our local machine:

```console
[qtc@kali ~]$ car run ssh
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_ssh_folder                /home/qtc/arsenal/ssh
[+]	car_ssh_port                  22
[+] 
[+] Running: sudo -E docker-compose up
Creating network "ssh_default" with the default driver
Creating car.ssh ... done
Attaching to car.ssh
car.ssh    | [+] IP address of the container: 172.23.0.2
car.ssh    | [+] No password was specified.
car.ssh    | [+] Generated random password for user 'default': Ne5IhtZ3
car.ssh    | [+] Adjusting volume permissions.
car.ssh    | [+] Creating login log.
car.ssh    | [+] Starting sshd
```

The *container configuration* maps the *ssh port* (``22``) to your local system:

```console
[qtc@kali ~]$ ss -tlnp
State                    Recv-Q                   Send-Q                                     Local Address:Port                                       Peer Address:Port
LISTEN                   0                        4096                                                   *:22                                                    *:*
```

On a remote host, we open a webserver listening on ``127.0.0.1:8000`` and attempt to forward
the corresponding port to the *ssh container*:

```console
[user@other ~]$ ssh 192.168.42.124 -l default -R 0.0.0.0:8000:127.0.0.1:8000
default@192.168.42.124's password:
4c8e831e9d2d:~ $
[...]
[user@other www]$ echo Hello World :D > test.txt
[user@other www]$ python3 -m http.server --bind 127.0.0.1 8000
Serving HTTP on 127.0.0.1 port 8000 (http://127.0.0.1:8000/) ...
```

From our local machine, we should now be able to access the forwarded port. However, notice that
the container is running in an *isolated network namespace*. Therefore, the forwarded port ``8000``
is not opened on your local machine, but on the container. You can use the containers IP address
to access it:

```console
[qtc@kali ~]$ curl 172.23.0.2:8000/test.txt
Hello World :D
```


### Enabling root login

----

Per default, only the user *default* can use *ssh* to connect to the container. This can be limiting, if you want to
forward privileged ports (e.g. ``445`` -> ``445``). To make this possible, you have to enable
*root login* on the container. You can do the following to achieve this:

1. Mirror the ssh container ``$ car mirror ssh``
2. Enable root login on the mirror ``$ cd ssh && bash toggle-root.sh``
3. Run the mirrored container ``$ car run .``

With root login enabled, the container will create a random password for the root account and allows root
logins via *ssh*. Please notice that allowing root access to a container has certain security implications
and is not considered best practice. Be careful with it and watch the server logs for unexpected root logins.


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``ssh_folder``: Top level resource folder of the container (used as docker volume).
* ``ssh_port``: SSH port that is opened on your local system.

You can also specify these options by using environment variables. The command ``car env ssh`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env ssh
[+] Available environment variables are:
[+] Name               Current Value                   Description
[+] car_ssh_folder     /home/qtc/arsenal/ssh           SSH resource folder. Mapped as a volume into the container.
[+] car_ssh_port       22                              SSH port mapped to your local machine.
[+] car_local_uid      1000                            UID of the SSH user.
```
