### FTP Container

----

The *ftp* container simply launches a *vsftpd* server and makes it accessible through your host system. 
The server can be accessed either *anonymously* or with *credentials*. 


### Anonymous Access

----

Anonymous access works as usual for other *FTP* servers. After the login, the anonymous user will
see two different directories:

```console
[qtc@kali ~]$ ftp 172.18.0.2
Connected to 172.18.0.2.
220 container arsenal FTP server
Name (172.18.0.2:qtc): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxrwxrwx    2 ftp      ftp          4096 Oct 17 22:31 anon
drwxr-x---    2 ftp      ftp          4096 Oct 17 22:31 user
226 Directory send OK.
```

In the *ftp-root* itself, the anonymous user does not have write access. This is for security reasons,
as the *vsftpd* server is using ``chroot`` to limit filesystem access. The anonymous user has only
write permissions to the ``anon`` directory.

```console
ftp> put test
local: test remote: test
200 PORT command successful. Consider using PASV.
553 Could not create file.
ftp> cd anon
250 Directory successfully changed.
ftp> put test
local: test remote: test
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
5 bytes sent in 0.00 secs (61.0352 kB/s)
```

### User Access

----

On startup, the container creates a user with name ``default`` and a randomly generated password:

```console
[qtc@kali ~]$ car run ftp
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_ftp_folder                /home/qtc/arsenal/ftp
[+]	car_anon_folder               /home/qtc/arsenal/ftp/anon
[+]	car_user_folder               /home/qtc/arsenal/ftp/user
[+]	car_ftp_port                  21
[+] 
[+] Running: sudo -E docker-compose up
Creating car.ftp ... done
Attaching to car.ftp
car.ftp    | [+] Creating default user...
car.ftp    | [+] No password was specified.
car.ftp    | [+] Generated random password for user 'default': 1dXq9QpS
car.ftp    | [+] Doing some config file magic...
car.ftp    | [+] Adjusting volume permissions...
car.ftp    | [+] Starting vsftpd.
```

After the login, also the user ``default`` is not able to write to the *ftp-root*. However, the
user ``default`` can use both directories ``anon`` and ``user`` for read and write operations.

```console
[qtc@kali ~]$ ftp 172.18.0.2
Connected to 172.18.0.2.
220 container arsenal FTP Server server
Name (172.18.0.2:qtc): default
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd user
250 Directory successfully changed.
ftp> put test
local: test remote: test
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
5 bytes sent in 0.00 secs (53.6573 kB/s)
```

### Networking Mode

----

Using *FTP* in combination with docker has some difficulties, as the *FTP* protocol uses additional ports apart from ``21`` for the
actual data transfer. These issues can be solved by applying specific options in the *vsftpd configuration file*. However,
as the main goal of *container-arsenal* is only to achieve file and process level *isolation*, the *ftp container* is run in *host networking mode*.
This means, that the network stack of the container is not *isolated*, but uses your ordinary *host network* instead. This solves
all networking related problems and *FTP* access over the network should work as the service would be running on your host system.


### Configuration Options

----

The following parameters can be modified inside the ``car.toml`` configuration file to adjust
the behavior of the container:

* ``ftp_folder``: This is the top level resource folder of the container.
* ``anon_folder``: This is the resource folder that is used for anonymous user uploads (mounted as volume into the container).
* ``user_folder``: This is the resource folder that is used for authenticated uploads (mounted as volume into the container).
* ``ftp_port``: The port where the *FTP* server is listening on your local machine.

You can also specify these options by using environment variables. The command ``car env ftp`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env ftp
[+] Available environment variables are:
[+] Name                               Current Value                      Description
[+] car_ftp_port                       21                                 FTP port mapped to your local machine.
[+] car_user_folder                    /home/qtc/arsenal/ftp/user         Volume location for the FTP user folder.
[+] car_anon_folder                    /home/qtc/arsenal/ftp/anon         Volume location for the FTP anonymous folder.
```
