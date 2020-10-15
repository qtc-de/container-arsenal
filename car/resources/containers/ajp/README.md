### AJP Proxy

----

The *ajp* container implements an *Apache2 AJP proxy* that forwards incoming requests to an *ajp* listener
on a different host. *AJP* is the *Apache JServ Protocol* and is used to establish a fast communication
channel between frontend and backend servers.

Then you install a *tomcat* server, the port ``8080`` is usually used for the webinterface. Additionally
the port ``8009`` is also opened by default and provides an *AJP* listener. While the webinterface at ``8080``
supports ordinary *HTTP* messages, the *AJP* listener on ``8009`` expects incoming messages to follow the
*AJP* specification. This is useful, in situations where you do not want *tomcat* as your frontend server.
In this case, you set up an ordinary *Apache2 web server* as the frontend and forward incoming requests to the
*tomcat* by using *AJP* on port ``8009``. Since the *AJP* protocol is a binary protocol, this is more efficient
than just forwarding plain *HTTP* messages.

Summarized: *AJP* is just another way to access the contents of a webserver. Sometimes you find the ordinary
webinterface of an application blocked (e.g. by firewall rules), but the *AJP* port is open. In these cases,
you can still perform some webserver enumeration on the *AJP* port.

That being said, all the ordinary tools usually focus on *HTTP* servers and are not compatible with *AJP*.
In these cases you can use this container. It opens a webserver on your local machine which forwards all
incoming requests to an *AJP* listener of your choice.


### Example

----

The following text describes an example usage. First of all, we start with the output of *nmap* for a *tomcat*
server with *AJP* enabled (notice that the webinterface is filtered and it is not possible to access the
*tomcat* via *HTTP*).

```console
[qtc@kali ~]$ nmap -p8009,8080 172.17.0.1
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-11 06:13 CEST
Nmap scan report for 172.17.0.1
Host is up (0.00011s latency).

PORT     STATE    SERVICE
8009/tcp open     ajp13
8080/tcp filtered http-proxy

Nmap done: 1 IP address (1 host up) scanned in 1.31 seconds
```

To access the *tomcat* server via *AJP*, we startup the *ajp* container of *container-arsenal*. However,
just running ``car run ajp`` is not sufficient in this case, as the container needs to know where to
redirect incoming *HTTP* requests. This can be configured either by running ``car mirror ajp`` and adjusting
the environment variable ``HOST`` within the ``docker-compose.yml`` file, or by specifying
the ``car_target_host`` environment variables during the startup:

```console
[qtc@kali ~]$ car_target_host=172.17.0.1 car run ajp
[+] Running: sudo car_ajp_folder=/home/qtc/arsenal/ajp car_log_folder=/home/qtc/arsenal/ajp car_target_port=8009 car_target_host=172.17.0.1 car_http_port=80 docker-compose up
Creating network "ajp_default" with the default driver
Creating car.ajp ... done
Attaching to car.ajp
car.ajp    | [+] Adjusting host and port values inside the jk_workes.properties file.
car.ajp    | [+] Adjusting volume permissions.
car.ajp    | [+] Starting AJP proxy server.
car.ajp    | [Sat Oct 10 07:31:13.102802 2020] [mpm_prefork:notice] [pid 9] AH00163: Apache/2.4.46 (Unix) mod_jk/1.2.48 configured -- resuming normal operations
car.ajp    | [Sat Oct 10 07:31:13.102823 2020] [core:notice] [pid 9] AH00094: Command line: 'httpd -D FOREGROUND'
```

Now we can access the *tomcat* server by using the webserver exposed by the container. You can either target the IP address of the container
directly or use the port that was mapped to your host system:

```html
[qtc@kali ~]$ ss -tlnp
State                    Recv-Q                   Send-Q                                     Local Address:Port                                       Peer Address:Port                   Process
LISTEN                   0                        4096                                           127.0.0.1:80                                              0.0.0.0:*

[qtc@kali ~]$ curl 127.0.0.1
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>HTTP Status 404 – Not Found</title>
    </head>
    <body>
        <h1>HTTP Status 404 – Not Found</h1>
        <hr class="line" />
        <p><b>Type</b> Status Report</p>
        <p><b>Message</b> Not found</p>
        <p><b>Description</b> The origin server did not find a current representation for the target resource or is not willing to disclose that one exists.</p>
        <hr class="line" />
        <h3>Apache Tomcat/9.0.30</h3>
    </body>
</html>
```

From the server banner at the end of the response you can see, that we are indeed talking to the *tomcat* server.


### Networking Mode

----

As network performance is relevant for the *ajp* container, the container runs with *host networking mode*. This means that the *network isolation* that *docker*
usually provides doesn't apply for this container. However, isolation for each other ressources like the file system or the process name space is still
in place.


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``http_port``: *HTTP* proxy port on your local machine.
* ``target_host``: Targeted server that exposes the *AJP* listener.
* ``target_port``: *AJP* port of the targeted server. Most of the times ``8009`` (the default) is what you want.
* ``ajp_folder``: Top level ressource folder of the *AJP* container.
* ``log_folder``: Folder where *mod_jk* logs are stored (volume).

You can also specify these options by using environment variables. The command ``car env ajp`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env ajp
[+] Available variables are:
[+] Name                               Current Value                      Description
[+] car_http_port                      80                                 HTTP proxy port on your local machine.
[+] car_log_folder                     /home/qtc/arsenal/ajp              Folder where mod_jk logs are stored (volume).
[+] car_target_host                    172.17.0.1                         Targeted server that exposes the AJP listener.
[+] car_target_port                    8009                               AJP port of the targeted server. Most of the times 8009 (the default) is what you want.
```
