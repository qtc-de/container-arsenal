## samba

This container starts a samba share that can be accessed over the SMB protocol. The server
exposes a public and a private share and does only expose port 445 and 139 on your local system.
The password for the private share is generated randomly on container startup.

With a guest account (no valid credentials) one can only access the public share. In this share,
uploading and downloading files is allowed for any user (or guest). The corresponding file storage
is the ``public`` resource folder of the container. The private share can only be accessed with valid credentials. The corresponding file storage is the 
``private`` resource folder of the container.


## Configuration Options

* samba_folder: Top level resource folder of the container.
* public_folder: Public resource folder.
* private_folder: Private resource folder.
* nb_port: NetBIOS port that is exposed on your local host.
* smb_port: SMB port that is exposed on your local host.
