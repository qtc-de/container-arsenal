### ssh

----

This container starts an alpine based ssh server with a single user account (username: default). 
The password for the user account is generated randomly and will be displayed
on container startup. The home folder of the user account will be mapped to the
top level resource folder of the container.


### Why it is useful?

----

An ssh client is available on almost all modern systems. Even for Windows it is more and more common
that an ssh client installation is present. Therefore, ssh is a good solution to:

* Upload/download files from/to the remote system.
* Forward ports using remote port forwarding.


### Enabling root login

----

Per default, only the user *default* can use ssh on the container. This can be limiting, if you want to
forward a port with a privileged port number (like 445 -> 445). To make this possible, you have to enable
root login on the container. You can do the following to achieve this:

1. Mirror the ssh container ``$ car mirror ssh``
2. Enable root login on the mirror ``$ cd ssh && bash toggle-root.sh``
3. Run the mirrored container ``$ car run .``

With root login enabled, the container will create a random password for the root account and allows root
logins via ssh. Please notice that allowing root access to a container has certain security implications
and is not considered best practice. Be careful with it and watch the server logs for unexpected root logins.


### Configuration Options

----

* ``ssh_folder``: Top level resource folder of the container.
* ``ssh_port``: SSH port that is exposed on your local system.
