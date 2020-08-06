### Container Arsenal

*container-arsenal* (*car*) is a collection of *docker containers* that have been proven to be useful during
security assessments / CTFs. Each container is represented by a *docker-compose* file and its corresponding
resources. Additionally, container arsenal ships a *Python* script that can be used to manage the
containers.

![](https://github.com/qtc-de/container-arsenal/workflows/master%20Python%20CI/badge.svg?branch=master)
![](https://github.com/qtc-de/container-arsenal/workflows/develop%20Python%20CI/badge.svg?branch=develop)


### Description

-----

During a security assessment it is often required to install additional services on your attacking machine.
Some common examples include:

* Hosting a FTP server to provide a payload that can be loaded via XXE.
* Hosting a SAMBA share to allow file sharing with a Windows machine.
* Hosting a WebDaV server to allow easy uploads from a remote host. 
* Hosting a ssh server to forward ports via remote port forwarding.
* Hosting an AJP proxy to connect to *tomcat's JSERV* ports.
* [...]

While I'm usually working on a VM with snapshots from a clean state, installing these kind of services
feels still wrong. I always get the feeling that I pollute my machine with stuff that I actually do not
want to be on it.

Docker becomes more and more popular among pentesters. To be honest, I think a lot of people overdo it a little
bit and when they start to run everything inside a dedicated container. However, for the services mentioned above,
Docker seems to be ideal to get an easy manageable solution.


### Installation

-----

*car* can be build and installed as a *pip package*. The following command installs *car* for your current user profile:

```console
$pip3 install car
```

You can also build *car* from source by running the following commands:

```console
$ git clone https://github.com/qtc-de/container-arsenal
$ cd container-arsenal
$ python3 setup.py sdist
$ pip3 install dist/*
```

Additionally, *car* ships a [bash-completion](./car/resources/bash_completion.d/car) script.
The completion script is installed automatically, but relies on the [completion-helpers](https://github.com/qtc-de/completion-helpers)
package. If *completion-helpers* is already installed, autocompletion for *car* should
work after installing the pip package. Otherwise, you may need to copy the completion
script manually:

```console
$ cp car/resources/bash_completion.d/car ~/.bash_completion.d
```

### Example Workflow

-----

Imagine you play a CTF and want to forward a port from a remote Linux host there you only have a non interactive reverse shell.
You can use a *SSH* server for this purpose and you want to create one quickly on the fly. With the *container-arsenal* installed,
you would just type:

```console
[pentester@kali ~]$ car run ssh
[+] Resource folder '/home/pentester/arsenal/ssh' does not exist.
[+] Creating new resource folder.
[+] Running: 'sudo car_ssh_folder=/home/pentester/arsenal/ssh car_ssh_port=22 docker-compose up'
Creating network "ssh_default" with the default driver
Creating car.ssh ... done
Attaching to car.ssh
car.ssh    | [+] IP address of the container: 172.19.0.2
car.ssh    | [+] No password was specified.
car.ssh    | [+] Generated random password for user 'default': 1C4GMsSq
car.ssh    | [+] Adjusting volume permissions.
car.ssh    | [+] Creating login log.
car.ssh    | [+] Starting sshd
```

And your ssh server is up and running. As you can see, a random 8-digit password is created automatically for the user *default*
and a resource folder on your local filesystem ``~/arsenal/ssh`` was created. To verify that everything is working one can ssh
into the container and create a file. The corresponding file can then be found inside the corresponding resource folder:

```console
[pentester@kali ~]$ ssh 127.0.0.1 -l default
default@127.0.0.1's password: 
~ $ echo test > file
~ $ Connection to 127.0.0.1 closed.
[pentester@kali ~]$ ls -l arsenal/ssh/file 
-rw-r--r-- 1 pentester pentester 5 Aug  6 18:00 arsenal/ssh/file
```

To stop the container, you can simply close it from the launching terminal by pressing ``ctrl-c`` or you launch ``car stop ssh``
from a different terminal.

```console
[pentester@kali ~]$ car stop ssh
[+] Running: 'sudo car_ssh_folder=/home/pentester/arsenal/ssh car_ssh_port=22 docker-compose stop'
Stopping car.ssh ... done
```

The resource folder of the corresponding container will stay alive and can be reused on the next startup. If you want to start with a 
clean resource folder, you could either remove it manually or run ``car clean ssh`` like in this example:

```console
[pentester@kali ~]$ car clean ssh
[+] Removing top level resource folder '/home/pentester/arsenal/ssh' (container: ssh)
```


### Available Containers

-----

The following paragraph lists all currently available containers inside the arsenal. Notice that each container folder contains a 
separate *README.md* where you can find more specific information about the corresponding container. Just click on the links listed
below:

* [ajp](car/resources/containers/ajp) - AJP proxy server to access JSERV ports via HTTP.
* [ftp](car/resources/containers/ftp) - vsftpd server that allows authenticated and anonymous access.
* [h2b](car/resources/containers/h2b) - A http-to-binary proxy that allows accessing non-HTTP services via HTTP.
* [mysql](car/resources/containers/mysql) - Just a mysql server with randomly generated, password protected user accounts.
* [neo4j](car/resources/containers/neo4j) - Plain Neo4j database. Useful for tools like BloodHound.
* [nginx](car/resources/containers/nginx) - nginx server with WebDav enabled. Supports HTTP and HTTPS.
* [samba](car/resources/containers/samba) - samba share that supports authenticated and anonymous access.
* [ssh](car/resources/containers/ssh) - ssh server with randomly generated user account. Remote port-forwarding is enabled.
* [tftp](car/resources/containers/tftp) - A simple tftp server.


### Configuration

-----

After installing the *container-arsenal*, a configuration file will be placed at ``~/.config/car/car.toml``. 
This configuration file contains default mappings for the provided containers. The configuration for the
**samba** container looks for example like this:

```toml
[containers]
  volume_base_path = "~/arsenal"

  [...]

  [containers.samba]
  samba_folder = "<@:BASE:@>/samba"
  public_folder = "<@:BASE:@>/samba/public"
  private_folder = "<@:BASE:@>/samba/private"
  nb_port= "139"
  smb_port = "445"
```

As you can see, the configuration file does specify a *volume_base_path*, which is by default set to ``~/arsenal``.
This is there your container volumes will be stored. The individual locations for the volumes are configured
in the different container sections. The above **samba** container will run with two volumes that will be mapped
to ``~/arsenal/samba/public`` and ``~/arsenal/samba/private``. 

The top level folder ``~/arsenal/samba`` is also included in the configuration file, but will not be mapped into
the container. Each container needs a top level folder definition with the naming scheme ``<CONTAINER_NAME>_folder``.
*car* needs this top level folder information for managing resource and permissions. For containers that do not
require subfolders, like the **ssh** container, a top level folder is even sufficient.

Internally, the folder definitions from the ``cat.toml`` file are just included into the ``docker-compose.yml``
file of the corresponding container. The ``docker-compose.yml`` of the **samba** container does look like this:

```yml
version: '3.7'

services:

  car.samba:
    container_name: car.samba
    image: car/samba
    build: .
    volumes:
      - ${car_public_folder}:/share/public
      - ${car_private_folder}:/share/private
      - ./scripts/start.sh:/scripts/start.sh
      - ./config/smb.conf:/config/smb.conf
      - ./config/supervisord.conf:/config/supervisord.conf
    ports:
      - "${car_nb_port}:139"
      - "${car_smb_port}:445"
```

If you want persistent configuration changes, the ``car.toml`` file is the correct location to make these. However,
sometimes you want only some quick changes that only apply for one particular situation. In this case, mirroring is the
recommended solution. As an example, imagine that I need a ssh container that is running on port 2222 instead of 22.
In this case, the first step I take is to mirror the ssh container:

```console
[pentester@kali ~]$ car mirror ssh
[+] Copying base folder of container 'ssh' to current working directory.
[+] Done.
[pentester@kali ~]$ ls -l ssh/
total 28
-rw-r--r-- 1 pentester pentester  849 Aug  6 17:57 Dockerfile
-rw-r--r-- 1 pentester pentester 1590 Aug  6 17:57 README.md
drwxr-xr-x 2 pentester pentester 4096 Aug  6 17:57 config
-rw-r--r-- 1 pentester pentester  382 Aug  6 18:05 docker-compose.yml
drwxr-xr-x 2 pentester pentester 4096 Aug  6 17:57 resources
drwxr-xr-x 2 pentester pentester 4096 Aug  6 17:57 scripts
-rwxr-xr-x 1 pentester pentester  913 Aug  6 17:57 toggle-root.sh
```

As you can see, mirroring just copies the directory of the corresponding docker container to your current working directory. Inside 
this directory you can find all files that were used for the container configuration. Inside the ``docker-compose.yml``
file, all environment variables that were mentioned before, are replaced by their default values. A mirrored ``docker-compose.yml``
looks therefore like this:

```yml
version: '3.7'

services:

  car.ssh:
    container_name: car.ssh
    image: car/ssh
    build: .
    volumes:
      - /home/pentester/arsenal/ssh:/home/default
      - ./scripts/start.sh:/scripts/start.sh
      - ./config/sshd_config:/etc/sshd/sshd_config
    ports:
      - "22:22"
```

If you want to apply your custom port change now, you can simply modify the mapping inside the ``docker-compose.yml`` and then run:

```console
[pentester@kali ssh]$ car run .
[+] Running: 'sudo docker-compose up'
Recreating car.ssh ... done
Attaching to car.ssh
car.ssh    | [+] IP address of the container: 172.19.0.2
car.ssh    | [+] No password was specified.
car.ssh    | [+] Generated random password for user 'default': uXWO2tDB
car.ssh    | [+] Adjusting volume permissions.
car.ssh    | [+] Creating login log.
car.ssh    | [+] Starting sshd
```

On another terminal, we can quickly verify that the ssh server is now exposed on port 2222:

```bash
[pentester@kali ~]$ ss -tln
State       Recv-Q      Send-Q           Local Address:Port           Peer Address:Port      Process      
LISTEN      0           128                    0.0.0.0:111                 0.0.0.0:*                      
LISTEN      0           4096                         *:2222                      *:*                      
LISTEN      0           128                       [::]:111                    [::]:*  
```


### Acknowledgements

-----

When creating the containers for this project I looked on many different repositories for useful Dockerfiles. Certain parts of the Dockerfiles
provided inside this repository are probably very similar to the one of other repositories. I did not wrote down all the references,
but If you think that your name should be listed here, feel free to contact me. 

For all the others I want to say thank your for providing access to their Dockerfiles on Github <3


### Further Notes

-----

The code of this repository was written on the fly. In some locations it is a little bit ugly and may contains some bugs. It could even be that
it harms your system, since user input from the ``car.toml`` file does not get sanitized and is used in ``subprocess`` calls from python. I will improve
the project in these regards and be happy for each suggestion. If you just use the version from this repository without any modifications on the ``car.toml``
file, it should be quite secure, but again: no guarantees!

*Copyright 2020, Tobias Neitzel and the container-arsenal contributors.*
