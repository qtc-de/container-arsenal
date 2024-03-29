# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2.2.0] - Apr 29, 2022

### Added

* Added a [php container](/car/resources/containers/php/)

### Changed

* The [nginx container](/car/resources/containers/php/) creates its TLS certificate
  now dynamically


## [2.1.0] - Apr 14, 2022

### Added

* Containers are now available as [GitHub packages](https://github.com/qtc-de?tab=packages&repo_name=container-arsenal).
* Added the `pull` action to pull containers from *GitHub*

### Changed

* Updated container base images to the most recent versions
* Disallow login on SSH container. Container can now only be used for remote portforwarding and file transfer (scp)
* Adjusted directory structure of nginx (required by current installed version)

### Removed

* Removed precompiled binaries (e.g. *AJP connector*). These are now compiled while building the containers


## [2.0.0] - Okt 22, 2020

### Added

* Add additional operations:
  * *env* (display available environment variables for a container)
  * *build* (build a container without running it)
  * *images* (show all already build containers)
  * *shell* (spawn an interactive shell in a running container)
  * *wipe* (remove a car container image)
* Add colored output.
* Add more detailed documentation for each container.
* Add non-sudo support (for users that are member of the docker group)
* Add arbitrary *UID* support. Previously, volume permissions were always set
  to ``1000:1000``, which was annoying when using a different *UID*. Now, *car* always
  uses your local *UID* (except you are *root*. In this case, *UID* ``1000`` is still the default).
* Add verbose logging for more containers (e.g. *ftp* and *tftp*, which not logged at all
  in previous versions).

### Changed

* Change some containers to operate in *Host Network Mode* per default. This increases
  the overall network performance and solves problems with random ports on the *(T)FTP*
  containers. Containers where performance does not matter were left in bridge mode.
* Changed calling convention for sudo calls to ``sudo -E``
* Improve container sizes:
  * **ajp**: ``236MB`` -> ``9.63MB`` (``~ 96%``)
  * **ftp**: ``9.95MB`` -> ``6.72MB`` (``~ 32%``)
  * **h2b** ``540MB`` -> ``53.3MB`` (``~ 90%``)
  * **nginx**: ``22.5MB`` -> ``10.2MB`` (``~ 55%``)
  * **samba**: ``105MB`` -> ``46.1MB`` (``~ 56%``)
  * **ssh**: ``16.6MB`` ->  ``11.7MB`` (``~ 30%``)
* *h2b* now supports *TLS* connections.
* *mysql* now starts with some default data you can perform tests against.
* *samba* does no longer include a *NETBIOS Name Server* (makes the container smaller).
* SSH works now with logging and *sftp*.
* removed *chisel* from the *ssh* container and from the complete repo history (just to big).
  Probably made some mistakes during the cleanup. Do not expect older versions to still
  function correctly :D


## [1.1.2] - Aug 8, 2020

### Changed

* Don't export the tests folder as a package during install.


## [1.1.1] - Aug 6, 2020

### Added

* Workflow for automatically pushing releases to PyPi

### Changed

* PyPi did not accept the project name *car*. It was changed to *container-arsenal*.


## [1.1.0] - Aug 6, 2020

### Added

* Add login monitoring for the ssh container
* Add root login on ssh container (but not default)
* Add statically compiled chisel on ssh container
* Add Python CI

### Changed

* AJP, H2B and Neo4j containers now bind to localhost only
* Improve bash completion script


## [1.0.0] - Nov 26, 2019

* Initial release :)
