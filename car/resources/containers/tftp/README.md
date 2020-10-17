### tftp

----

This container starts a *tftp* server that allows uploads and downloads using the *TFTP* protocol.
The corresponding storage location is mapped to the top level resource folder of the container
and can be accessed from your local host system (docker volume).


### Example Usage

----

First of all, we start the container on out local machine:

```console
[qtc@kali ~]$ car run tftp
[+] Environment Variables:
[+]	car_tftp_folder               /home/qtc/arsenal/tftp
[+]	car_tftp_port                 69
[+]
[+] Running: sudo -E docker-compose up
Creating car.tftp ... done
Attaching to car.tftp
car.tftp    | [+] Adjusting volume permissions.
car.tftp    | [+] Starting tftpd.
```

This should open the *UDP* port ``69`` (default *TFTP* port) on your local machine:

```console
[qtc@kali ~]$ ss -ulnp
State                    Recv-Q                   Send-Q                                     Local Address:Port                                       Peer Address:Port                   Process
UNCONN                   0                        0                                                0.0.0.0:69                                              0.0.0.0:*
```

From a different host, you can now attempt to upload a file:

```console
[qtc@other ~]$ echo Hello World :D > test.txt
[qtc@other ~]$ tftp 192.168.42.124
tftp> put test.txt
Sent 16 bytes in 0.0 seconds
```

On your host system, you should be able to find this file in your resource folder (e.g. ``~/arsenal/tftp``):

```console
[qtc@kali ~]$ cat arsenal/tftp/test.txt
Hello World :D
```


### Networking Mode

----

Using *TFTP* in combination with docker has some difficulties, as the *TFTP* protocol uses additional ports apart from *69 (UDP)* for the
actual data transfer. These issues can be solved by applying specific options to the *tftp daemon* (namely adjusting *port-range*). However,
as the main goal of *container-arsenal* is to achieve file and process level *isolation*, the *tftp container* is run in *host networking mode*.
This means, that the network stack of the container is not *isolated*, but uses your ordinary *host network* instead. This solves
all networking concerned problems.


### Configuration Options:

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``tftp_folder``: Top level resource folder of the container (volume).
* ``tftp_port``: *TFTP* port that will be opened on your local machine.

You can also specify these options by using environment variables. The command ``car env tftp`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env tftp
[+] Available environment variables are:
[+] Name                Current Value                    Description
[+] car_tftp_port       69                               TFTP port opened on your local machine.
[+] car_tftp_folder     /home/qtc/arsenal/tftp           TFTP root folder used as volume in the container.
```
