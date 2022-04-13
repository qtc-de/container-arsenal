### TFTP

----

This container starts a *TFTP* server that allows uploads and downloads using the *TFTP* protocol.
The corresponding storage location is mapped to the top level resource folder of the container
and can be accessed from your local host system (e.g. ``~/arsenal/tftp/``).


### Example Usage

----

First of all, we start the container on our local machine:

```console
[qtc@devbox ~]$ car run tftp
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_tftp_folder               /home/qtc/arsenal/tftp
[+]	car_tftp_port                 69
[+] 
[+] Running: sudo -E docker-compose up
Creating car.tftp ... done
Attaching to car.tftp
car.tftp    | [+] Adjusting volume permissions.
car.tftp    | [+] Starting tftpd.
```

This should open the *UDP* port ``69`` (default *TFTP* port):

```console
[qtc@devbox ~]$ ss -ulnp
State                    Recv-Q                   Send-Q                                     Local Address:Port                                       Peer Address:Port
UNCONN                   0                        0                                                0.0.0.0:69                                              0.0.0.0:*
```

From a different host, we can now attempt to upload a file:

```console
[user@other ~]$ echo Hello World :D > test.txt
[user@other ~]$ tftp 192.168.42.124
tftp> put test.txt
Sent 16 bytes in 0.0 seconds
```

Back on our local machine, we should be able to find the uploaded file within our *tftp resource folder*
(e.g. ``~/arsenal/tftp``):

```console
[qtc@devbox ~]$ cat arsenal/tftp/test.txt
Hello World :D
```


### Networking Mode

----

Using *TFTP* in combination with docker has some difficulties, as the *TFTP* protocol uses additional ports apart from *69 (UDP)* for the
actual data transfer. These issues can be solved by applying specific options to the *tftp daemon* (namely adjusting the *port-range*). However,
as the main goal of *container-arsenal* is to achieve file and process level *isolation*, the *tftp container* is run in *host networking mode* instead.
This means, that the network stack of the container is not *isolated*, but uses your ordinary *host network*. This solves all networking concerned problems
and *TFTP* connections should work as the service would be running on your host system.


### Configuration Options:

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``tftp_folder``: Top level resource folder of the container (volume).
* ``tftp_port``: *TFTP* port that will be opened on your local machine.

You can also specify these options by using environment variables. The command ``car env tftp`` explains their corresponding usage:

```console
[qtc@devbox ~]$ car env tftp
[+] Available environment variables are:
[+] Name                Current Value                    Description
[+] car_tftp_port       69                               TFTP port opened on your local machine.
[+] car_tftp_folder     /home/qtc/arsenal/tftp           TFTP root folder used as volume in the container.
[+] car_local_uid       1000                             UID of the TFTP user.
```
