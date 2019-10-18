## ssh

This container starts an alpine based ssh server with a single user account. 
The password for the user account is generated randomly and will be displayed
on container startup. The home folder of the user account will be mapped to the
top level resource folder of the container.

## Why it is useful?

The ssh server can be used to upload some files from a remote host via scp. Furthermore,
you can tunnel some network traffic using remote port forwarding.

## Configuration Options

* ssh_folder: Top level resource folder of the container.
* ssh_port: SSH port that is exposed on your local system.
