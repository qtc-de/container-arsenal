### tftp

----

This container starts a *tftp* server that allows uploads and downloads using the *TFTP* protocol.
The corresponding storage location is mapped to the top level resource folder of the container
and can be accessed from your local host system (docker volume).


### Example Usage

----



## Configuration Options:

* tftp_folder: Top level resource folder of the container.
* tftp_port: TFTP port that will be exposed on your local host.
