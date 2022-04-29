### h2b (HTTP to Binary)

----

This *docker container* implements a proxy server that forwards the body of incoming *HTTP* requests to a different host.
The response from the targeted server is encapsulated into a *HTTP* response message and send back to the client.
To specify a target, simply use the two *GET* parameters ``host`` and ``port`` inside of the *HTTP* request. The
body of the *HTTP* request is then forwarded to the specified target.

Currently the container is running the *Flask development server*. I guess this should be sufficient for the purpose of this project.
However, one could also set up a *nginx reverse-proxy* in front of the actual application, but this is probably an overkill.
In future, the *Flask* application may be replaced with an optimized binary for handling *HTTP* requests. Since most *HTTP* features
are not required for the proxy functionality, this should greatly reduce the container size. The advantage of the *Flask* application,
on the other hand, is that you can add modifications and debugging statements pretty easily.


### Example Usage

----

In the following, an example usage of the container is demonstrated. First of all, the container needs to be started:

```console
[qtc@devbox ~]$ car run h2b
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_h2b_folder                /home/qtc/arsenal/h2b
[+]	car_http_port                 8001
[+]
[+] Running: sudo -E docker-compose up
Creating car.h2b ... done
Attaching to car.h2b
car.h2b    |  * Serving Flask app "h2b.py"
car.h2b    |  * Environment: production
car.h2b    |    WARNING: This is a development server. Do not use it in a production deployment.
car.h2b    |    Use a production WSGI server instead.
car.h2b    |  * Debug mode: off
car.h2b    |  * Running on http://127.0.0.1:8001/ (Press CTRL+C to quit)
```

In order to provide the target server, a *netcat* listener within the local network is started on ``192.168.42.139:4444``:

```console
[user@other ~]$ nc -vlp 4444
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
```

Now we can send a *POST* request, containing the remote target within the ``host`` and ``port`` *GET* parameters, to
the proxy port (default: ``8001``).  The body of the *POST* request should be forwarded and arrive at the *netcat listener*.

```console
[qtc@devbox ~]$ curl -X POST 'http://127.0.0.1:8001/forward?host=192.168.42.139&port=4444' -d "Example Message"
[...]

[user@other ~]$ nc -vlp 4444
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.42.1.
Ncat: Connection from 192.168.42.1:50298.
Example Message
```

When responding to this message in the *netcat* terminal, the final content will be passed back as *HTTP response*:

```console
[user@other ~]$ nc -vlp 4444
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.42.1.
Ncat: Connection from 192.168.42.1:50298.
Example Message
Hi :D
[user@other ~]$
[...]

[qtc@devbox ~]$ curl -X POST 'http://127.0.0.1:8001/forward?host=192.168.42.139&port=4444' -d "Example Message"
Hi :D
```

When you are facing a *SSL* protected service, you can specify ``ssl=true`` as an additional *GET* parameter.
The forwarded connection is then made using *SSL* without applying certificate validation.


### Why it is useful?

----

A lot of tools are specially focused on *HTTP*, but could also be useful in other situations. As an example, consider *sqlmap*.
Recently I saw a service that communicated by using plain *XML* messages. A valid request looked like this:

```xml
<search>
  <filter>
    <name>
      test
    </name>
  </filter>
</search>
```

It was rather easy to identify that the ``<name>-tag`` is vulnerable to *SQL injection* attacks, but the injection was blind and it was difficult
to extract information from the database. It would be great to use *sqlmap* in these situations, but as far as I know, *sqlmap* does not
support *non-HTTP* protocols.

By using this docker container, you can simply solve the above mentioned problem. First of all, you wrap the *XML* message mentioned above
inside a *HTTP POST* request. Instead of using this request with *sqlmap* against the targeted service directly, you use it against this docker
container and specify the targeted host and port by using the corresponding *GET* parameters inside the *HTTP* request.


### Limitations

----

In the current state, the proxy does only support stateless protocols / connections. If the targeted service wants to keep the *TCP* channel
opened and does not act stateless, this container will currently not work.

One could try to implement support for statefull protocols / connections, but it is difficult. Theoretically, the socket of the *TCP* connection
can be stored by the server (e.g. in form of a *session-storage*), but if the targeted protocol is unknown, it is difficult to implement the correct
message flow.

In future, support for some known statefull protocols may be added. Feel free to contribute.


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` file:

* ``h2b_folder``: Top level ressource folder of the container. In the current configuration this folder is not used.
* ``http_port``: *HTTP* port of the proxy that is opened on your local machine.

You can also specify these options by using environment variables. The command ``car env h2b`` explains their corresponding usage:

```console
[qtc@devbox ~]$ car env h2b
[+] Available environment variables are:
[+] 
[+] Name               Current Value             Description
[+] car_http_port      8001                      HTTP proxy port opened on your local machine.
```
