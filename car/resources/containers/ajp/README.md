## ajp

The ajp container implements an apache2 AJP proxy that forwards incoming requests to an ajp listener. 
For all how do not know what AJP actually is, it is the *Apache JServ Protocol* and is used to establish a 
fast communication channel between frontend and backend servers.

Then you install a Tomcat server listening on port *8080* for example, often the port *8009* is also opened.
While the port *8080* does support ordinary HTTP messages, *8009* expects incoming messages to follow the
AJP standard. This is useful in situations where you do not want the Tomcat server as your Frontend server.
In this case, you set up an ordinary Apache2 server as the frontend and forward incoming requests to your
Tomcat server on port *8009*. Since the AJP protocol is a binary protocol, this is more efficient than forwarding
the plain HTTP message.

If you find port *8009* (or another AJP speaking port) exposed on a server, you can simply start this docker container
and use it as a proxy to communicate to your target via plain HTTP.


## Why it is useful?

In some situations the actual HTTP port of a Tomcat server is not exposed, but the AJP port is available. In these situations
you may be able to access webpages that should actually be not accessible. 

Another interisting situation is that certain URLs may be blocked on the HTTP port, while being accessible on the AJP port.
A common example is of course the ``/manager`` endpoint of the tomcat server.


## Configuration Options

* ajp_folder: Top level ressource folder of the AJP container. In this folder, log files of AJP will be stored.
* target_port: AJP port of the targeted server. Using a default value here does not make sense. Either adjust the
  value inside your *car.toml* file or mirror the ajp container depending on your current target.
* target_host: Targeted server which exposes the AJP port. Using a default value here does not make sense. Either adjust the
  value inside your *car.toml* file or mirror the ajp container depending on your current target.
* http_port: The HTTP port there the ajp container does expose the proxy interface. Use this port to forward HTTP requests to
  the targeted server.
