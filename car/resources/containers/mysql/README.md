### MySQL (MariaDB)

----

The *mysql* container does simply start a *mysql* server with a root and one low privileged account. 
To be honest, it is not super useful, but sometimes I want to test some queries or try to connect
some remote services with my own database. Therefore, the container can safe some time in these specific
situations.


### Container Size Considerations

----

It is possible to reduce the container size of a *mariadb* quite a bit. By installing the
*mariadb* package on a plain *alpine* image, the resulting container size is around ``200MB``.
This is way smaller than the size of the official *mariadb* container, that is around ``350MB``.

However, I decided that for container sizes that are larger than ``50MB`` I will use the official
images instead of creating custom ones. No matter if ``200MB`` or ``350MB``, both are quite large,
but the official image is more likely to be resued by other containers or projects on your system.
Therefore, sticking to the official images in these cases is probably more memory efficient in the
long term.


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` file:

*  ``mysql_port``: *MySQL* port that is mapped to your local machine.
*  ``mysql_folder``: Top level resource folder. All database relevant data is stored here.
*  ``root_password``: Password of the root user account (randomly generated if not specified)
*  ``user_password``: Password of the low privileged user account (randomly generated if not specified)

In contrast to the [neo4j](../neo4j) container, the *mysql* passwords will not change when the container
is started with a pre-existent *mysql* database. You can also specify these options by using environment
variables. The command ``car env mysql`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env ajp
[+] Available variables are:
[+] Name                               Current Value                      Description
[+] car_http_port                      80                                 HTTP proxy port on your local machine.
[+] car_log_folder                     /home/qtc/arsenal/ajp              Folder where *mod_jk* logs are stored.
[+] car_target_host                    172.17.0.1                         Targeted server that exposes the *AJP* listener.
[+] car_target_port                    8009                               AJP port of the targeted server. Most of the times 8009 (the default) is what you want.
```
