## h2b (HTTP to Binary)

This docker container implements a proxy server which forwards the body of incoming HTTP requests to a different host.
The response from the targeted server is encapsulated into a HTTP message and send back to the client. To specify a target,
simply send the two GET parameters **host** and **port** inside your HTTP request. The body of the HTTP request is then
forwarded to the corresponding target.

Currently the container is running the Flask development server. I guess this should be sufficient for the purpose of this project.
However, one could also set up a **nginx** reverse-proxy in front of the actual application, but I think it is an overkill.


## Why it is useful?

A lot of pentesting tools are specially focused on HTTP, but could also be useful in other situations. As an example, consider **sqlmap**.
Recently I found a port on a system that communicated by using plain XML messages. A valid request looked something like this:

```xml
<search>
  <filter>
    <name>
      test
    </name>
  </filter>
</search>
```

It was rather easy to identify that the '\<name\>' tag is vulnerable to SQLi attacks, but the injection was blind and it was difficult
to extract information from the database. It would be great to use sqlmap in these situations, but as far as I know, sqlmap does not
support non-HTTP protocols. 

By using this docker container, you can simply solve the above mentioned problem. First of all, you wrap the XML message mentioned above
inside a HTTP POST request. Instead of using this request with sqlmap against the targeted host directly, you use it against this docker
container and specify the targeted host and port by using the corresponding GET parameters inside the HTTP request.

## Limitations

In the current state, the proxy does only support stateless protocols / connections. If the targeted service wants to keep the TCP channel
opened and does not act stateless, this container will currently not work. 

One could try to implement support for statefull protocols / connections, but it is difficult. Theoretically, the socket of the TCP connection
can be stored by the server (e.g. in form of a session-storage), but if the targeted protocol is unknown, it is difficult to implement a correct 
message flow.

In future, support for some known statefull protocols may be added. Feel free to contribute.


## Configuration Options

* h2b_folder: Top level ressource folder of the container. In the current configuration this folder is not used.
* http_port: HTTP port of the container that exposes the proxy interface.
