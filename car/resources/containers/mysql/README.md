### MySQL (MariaDB)

----

The *mysql* container simply starts a *MySQL* server with a root and one low privileged account. 
To be honest, it is not super useful, but sometimes I want to test some queries or try to connect
some remote services with my own database. In these cases, the container can safe some time.

To make it a little bit more useful, the container sets up a default database on startup and populates
it with some data. By default, the ``default.users`` table is created with the following contents:

```
SELECT * FROM default.users\G;

*************************** 1. row ***************************
      id: 1
username: admin
   email: admin@container-arsenal.de
password: 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
*************************** 2. row ***************************
      id: 2
username: user
   email: user@container-arsenal.de
password: d015cc465bdb4e51987df7fb870472d3fb9a3505
*************************** 3. row ***************************
      id: 3
username: bob
   email: bob@bobbobbobbob.bob
password: 48181acd22b3edaebc8a447868a7df7ce629920a
```


### Container Size Considerations

----

It is possible to reduce the container size of a *mariadb* quite a bit. By installing the
*mariadb* package on a plain *alpine* image, the resulting container size is around ``200MB``.
This is way smaller than the size of the official *mariadb* container, which is around ``350MB``.

However, I decided that for container sizes that are larger than ``50MB`` I will use the official
images instead of creating custom ones. No matter if ``200MB`` or ``350MB``, both are quite large,
but the official image is more likely to be reused by other containers or projects on your system.
Therefore, sticking to the official images in these cases is probably more memory efficient in the
long term.

There are also some custom *mariadb* images available on *Docker Hub* that manage to reduce the container
size below ``50MB``. However, these images often strip functionalities or modify other internals. While
the low size of ``50MB`` is very tempting, I fear that these modifications could be annoying when testing
*SQL* queries, as in these cases you usually want the database to behave like the official image.


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` file:

*  ``mysql_port``: *MySQL* port that is mapped to your local machine.
*  ``mysql_folder``: Top level resource folder. All database relevant data is stored here (volume).
*  ``root_password``: Password of the root user account (randomly generated if not specified).
*  ``mysql_password``: Password of the low privileged user account (randomly generated if not specified).
*  ``mysql_user``: Username of the low privileged account (default, by default).
*  ``mysql_database``: *MySQL* database name (default, by default).

In contrast to the [neo4j](../neo4j) container, *MySQL* passwords will not change when the container
is started with a pre-existent *MySQL* database. If you want to start from a clean instance, you should
run ``car clean mysql`` first. You can also specify container options by using environment
variables. The command ``car env mysql`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env mysql
[+] Available environment variables are:
[+] Name                               Current Value                      Description
[+] car_mysql_user                     default                            MySQL user that is created for database access.
[+] car_mysql_port                     127.0.0.1:3306                     MySQL port that is mapped to your local system.
[+] car_mysql_folder                   /home/qtc/arsenal/mysql            Local folder where database contents are stored (volume).
[+] car_root_password                                                     Password for the MySQL root account.
[+] car_mysql_database                 default                            MySQL database that is created during startup.
[+] car_mysql_password                                                    Password for the default MySQL user account.
```
