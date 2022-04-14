### Neo4j

----

*Neo4j* is a *graph database* that is (among others) required by *BloodHound*. After running
``car run neo4j`` the database starts in a dedicated container and the *HTTP* port (``7474``)
and the *BOLT* port (``7687``) are mapped to your local system. The password for the *neo4j*
user is assigned randomly and is regenerated during each container startup.


### Container Size Considerations

----

The official base image of *neo4j* is quite large in memory size (around ``500MB``). By manually
installing it on a *alpine* container and applying some patches (removing demos and not required
parts of the ``JRE``), one can reduce the image size to about ``200MB``. Other custom builds
on *Docker Hub* may achieve an even more reasonable compression (probably even below ``50MB``).

While this is a reasonable amount of saved memory, I decided to stick with the base image. No matter
if ``200MB`` or ``500MB``, both images are quite large, but the official image is more likely to
being reused by other tools or containers. Therefore, even using the larger image could be more
memory saving in the long term. Custom builds with certain files being removed may break in some
edge cases. Missing a vulnerability because the database did not work as expected would be a great
issue.


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``neo4j_folder``: Top level resource folder of *neo4j*. All database relevant data will be stored here.
* ``http_port``: *HTTP* port of *neo4j* that will be mapped on your local system.
* ``bolt_port``: *BOLT* port of *neo4j* that will be mapped on your local system.

In contrast to the [MySQL container](../mysql), the password will reset on each database startup and a new randomly
generated password is used. If this is annoying for you, you can change the behavior inside the [startup script](./scripts/start.sh).
You can also specify options by using environment variables. The command ``car env ajp`` explains their corresponding usage:

```console
[qtc@devbox ~]$ car env neo4j
[+] Available environment variables are:
[+] Name                 Current Value                     Description
[+] car_http_port        127.0.0.1:7474                    HTTP port for neo4j webinterface mapped to your local machine.
[+] car_bolt_port        127.0.0.1:7687                    BOLT port for Bloodhound access mapped to your local machine.
[+] car_neo4j_folder     /home/qtc/arsenal/neo4j           Folder where the neo4j database is stored (volume).
[+] car_local_uid        1000                              UID of the neo4j user.
```
