### Container Arsenal

----

*container-arsenal* (*car*) is a collection of *docker containers* that have been proven to be useful during
security assessments and *CTFs*. Each container is represented by a *docker-compose* file and its corresponding
resources. Additionally, *container-arsenal* ships a *python* script that can be used to manage the containers.

![](https://github.com/qtc-de/container-arsenal/workflows/master%20Python%20CI/badge.svg?branch=master)
![](https://github.com/qtc-de/container-arsenal/workflows/develop%20Python%20CI/badge.svg?branch=develop)
[![](https://img.shields.io/badge/version-2.1.0-blue)](https://github.com/qtc-de/container-arsenal/releases)
[![](https://img.shields.io/badge/build%20system-pip-blue)](https://pypi.org/project/pip/)
![](https://img.shields.io/badge/python-9%2b-blue)
[![](https://img.shields.io/badge/license-GPL%20v3.0-blue)](https://github.com/qtc-de/container-arsenal/blob/master/LICENSE)



https://user-images.githubusercontent.com/49147108/163109100-3da4697b-05e2-43a5-a7f0-c0005e64c326.mp4



### Installation

-----

*container-arsenal* can be build and installed using *pip*. The following command installs *container-arsenal*
for your current user profile:

```console
$ pip3 install --user container-arsenal
```

You can also build *container-arsenal* from source by running the following commands:

```console
$ git clone https://github.com/qtc-de/container-arsenal
$ cd container-arsenal
$ python3 setup.py sdist
$ pip3 install dist/*
```

*container-arsenal* ships an [autocompletion script](car/resources/bash_completion.d/car) for bash. With the
[completion-helpers](https://github.com/qtc-de/completion-helpers) project installed, the completion script is
setup automatically during the installation of *container-arsenal*. You can also install the *completion-helpers*
project later on and copy the [completion script](car/resources/bash_completion.d/car) to your `~/.bash_completion.d`
folder manually.


### Available Containers

----

The following list provides an overview on the currently available containers. Notice that each container folder contains a
dedicated ``README.md`` where you can find more specific information about the corresponding container. Just click on the
links listed below to get more details:

**File Transfer Containers**

* [ftp](car/resources/containers/ftp) - *vsftpd* server configured for authenticated and anonymous access
* [tftp](car/resources/containers/tftp) - A simple *tftp* server for *UDP* based file exchange
* [nginx](car/resources/containers/nginx) - *nginx* server with *WebDAV* enabled. Supports *HTTP* and *HTTPS*
* [samba](car/resources/containers/samba) - *Samba* share configured for authenticated and anonymous access
* [ssh](car/resources/containers/ssh) - *SSH* server that allows *remote port-forwarding* and *scp*

**Proxy Containers**

* [ajp](car/resources/containers/ajp) - *AJP* proxy server to access *JSERV* ports via *HTTP*
* [h2b](car/resources/containers/h2b) - A *http-to-binary* proxy that allows accessing *non-HTTP* services using *HTTP* focused tools

**Utils Containers**

* [mysql](car/resources/containers/mysql) - Plain *MySQL* server with randomly generated password protected user accounts.
* [neo4j](car/resources/containers/neo4j) - Plain *Neo4j* database. Useful for tools like *BloodHound*


### Getting and Updating Containers

----

*container-arsenal* provides a prebuild version for all available containers within the [repository packages](https://github.com/qtc-de?tab=packages&repo_name=container-arsenal)
You can pull these images using the following commands:

```console
[qtc@devbox ~]$ car pull ssh          # Just pulls the ssh container
[qtc@devbox ~]$ car pull all          # Pulls all containers
```

Instead of pulling prebuild containers, you can also build them locally by using the *build* action:

```console
[qtc@devbox ~]$ car build ssh         # Just builds the ssh container
[qtc@devbox ~]$ car build all         # Builds all containers
```

Building the containers locally has the advantage that the corresponding software is installed from scratch
and associated files and resources are not publicly available, as it is the case for the prebuild containers.
Moreover, building locally installs the most recent version of the corresponding software, while prebuild
containers use the most recent software version that was available on their build date. Therefore, using
locally build containers may be preferred in security critical contexts.


### Configuration

----

After installing *container-arsenal*, a configuration file will be placed at ``~/.config/car/car.toml``.
This configuration file contains some global variables and default mappings for the provided containers.
The first few lines look like this:

```toml
[containers]
  sudo_required = true
  volume_base_path = "~/arsenal"
```

The `[containers]` section contains parameters that apply to all available containers. The `sudo_required`
setting determines whether *docker commands* have to be prefixed with `sudo`, whereas the `volume_base_path`
specifies the default local directory where *docker volumes* will be stored.

Apart from global configuration options, the ``car.toml`` file also contains container specific options.
The following snipped shows the configuration for the *samba* container:

```toml
[containers.samba]
samba_folder = "<@:BASE:@>/samba"
public_folder = "<@:BASE:@>/samba/public"
private_folder = "<@:BASE:@>/samba/private"
smb_port = "445"
```

This configuration shows, that the *samba* container runs with two volumes that will be mapped to
``~/arsenal/samba/public`` and ``~/arsenal/samba/private``. The top level folder ``~/arsenal/samba``
is also included in the configuration file, but will not be mapped into the container. 


### Acknowledgements

-----

When creating the containers for this project I searched many different repositories for useful *Dockerfiles*. Certain parts of the *Dockerfiles*
provided inside this repository are probably very similar to others that can be found on *GitHub*. I did not wrote down all the references,
but if you think that your name should be listed here, feel free to contact me :)

For all others: thank you for working on open source projects <3

*Copyright 2022, Tobias Neitzel and the container-arsenal contributors.*
