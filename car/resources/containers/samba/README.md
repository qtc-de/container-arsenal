### Samba

----

This container starts a *Samba share* that can be accessed via the *SMB protocol*. The server
exposes a *public* and a *private share* and does only map port *445* to your local system.
The password for the *private share* is generated randomly during container startup and
the corresponding username is ``default``.

Without valid credentials, it is only possible to access the *public share*. The *public share*
allows uploading and downloading files for any user (or guest). The corresponding file storage
is the ``public`` resource folder of the container (e.g. ``~/arsenal/samba/public``). The private
share can only be accessed with valid credentials. The corresponding file storage is the 
``private`` resource folder of the container (e.g. ``~/arsenal/samba/private``).


### Example Usage

----

In the following an example usage of the container is demonstrated. First of all, we start the
container:

```console
[qtc@kali ~]$ car run samba
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_samba_folder              /home/qtc/arsenal/samba
[+]	car_public_folder             /home/qtc/arsenal/samba/public
[+]	car_private_folder            /home/qtc/arsenal/samba/private
[+]	car_smb_port                  445
[+] 
[+] Running: sudo -E docker-compose up
Creating network "samba_default" with the default driver
Creating car.samba ... done
Attaching to car.samba
car.samba    | [+] No password was specified.
car.samba    | [+] Generated random password for user 'default': 4ongYvsA
car.samba    | [+] Adjusting volume permissions.
car.samba    | [+] Starting samba service.
car.samba    | smbd version 4.12.7 started.
```

Notice that the network shares opened by the container are not browsable.
Therefore, the following output is expected and the *public* and *private*
shares exist, although not being visible.

```console
[qtqc@kali ~]$ smbclient -L //127.0.0.1 -N

	Sharename       Type      Comment
	---------       ----      -------
	IPC$            IPC       IPC Service (car SMB sever)
```

Now we try to upload a file to the *public share* from a *Windows host* within our network:

```console
C:\Users\qtc>echo Hello World :D > test.txt
C:\Users\qtc>copy test.txt \\192.168.42.124\public
        1 file(s) copied.
```

Back on our machine, we can verify that the file arrived in the resource folder of the *public share*:

```console
[qtc@kali ~]$ cat ~/arsenal/samba/public/test.txt 
Hello World :D
```

By using the credentials generated during container startup, we could also
access the *private share*:

```console
C:\Users\qtc>net use Y: \\192.168.42.124\private /user:default 4ongYvsA
The command completed successfully.
C:\Users\qtc>copy test.txt Y:
        1 file(s) copied.
```

Back on our local machine, the file is available in the resource folder of the *private share*:

```console
[qtc@kali ~]$ cat ~/arsenal/samba/private/test.txt 
Hello World :D 
```

### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``smb_port``: *SMB* port that is mapped to your local machine.
* ``samba_folder``: Top level resource folder of the container.
* ``public_folder``: Public resource folder mapped into the container (volume).
* ``private_folder``: Private resource folder mapped into the container (volume).

You can also specify these options by using environment variables. The command ``car env samba`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env samba
[+] Available environment variables are:
[+] Name                   Current Value                             Description
[+] car_smb_port           445                                       SMB port that is mapped to your local machine.
[+] car_public_folder      /home/qtc/arsenal/samba/public            Public resource folder mapped into the container (volume).
[+] car_private_folder     /home/qtc/arsenal/samba/private           Private resource folder mapped into the container (volume).
[+] car_local_uid          1000                                      UID of the SMB user.
```
