### PHP

----

The *php* container starts an *Nginx* webserver that maps an *HTTP* and an *HTTPS* port to your local system. 
Beside providing an easy way for file downloads, the server has *php* enabled and allows you to serve the output
of *php* scripts to incoming client connections. This can be useful for testing certain *php* actions locally
or when you need to serve dynamically created content to a client.

Downloadable files and *php* scripts need to be placed in one of the resource folders (`~/arsenal/php/public` or
`~/arsenal/php/private`). The `public` folder is accessible via *HTTP(S)* without any restrictions. The `private`
folder requires *Basic authentication* using a password that is randomly generated at container startup. To prevent
some dangerous mistakes, the container binds only to localhost per default. You need to modify your `car.toml` or
set the corresponding `car_http_port` and `car_https_port` environment variables to expose it to other interfaces.


### Example Usage

----

In the following you find a short example usage. First of all, the *php* container is started:

```console
[qtc@devbox ~]$ car run php
[+] Environment Variables:
[+]	car_local_uid                 1000
[+]	car_php_folder                /home/qtc/arsenal/php
[+]	car_public_folder             /home/qtc/arsenal/php/public
[+]	car_private_folder            /home/qtc/arsenal/php/private
[+]	car_http_port                 127.0.0.1:80
[+]	car_https_port                127.0.0.1:443
[+] 
[+] Running: docker-compose up
Starting car.php ... done
Attaching to car.php
car.php    | [+] Adjusting UID values.
car.php    | [+] No password was specified.
car.php    | [+] Generated random password: XhmSAti8
car.php    | [+] Creating .htpasswd file.
car.php    | [+] Access to /private allowed for: default:XhmSAti8
car.php    | [+] Starting php-fpm8.
car.php    | [+] Starting nginx daemon
```

Now we can place a simple *PHP* script within the `public` folder and access it via *HTTP*:

```console
[qtc@devbox ~]$ echo '<? echo "Hello World :D\n" ?>' > arsenal/php/public/hello.php
[qtc@devbox ~]$ curl http://127.0.0.1/hello.php
Hello World :D
```

When placing the script in the `private` folder instead, we need to specify credentials
before we can access the script:

```console
qtc@devbox ~]$ echo '<? echo "Hello World :D\n" ?>' > arsenal/php/private/hello.php
[qtc@devbox ~]$ curl http://127.0.0.1/private/hello.php
<html>
<head><title>401 Authorization Required</title></head>
<body>
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx</center>
</body>
</html>
[qtc@devbox ~]$ curl http://default:XhmSAti8@127.0.0.1/private/hello.php
Hello World :D
```


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``php_folder``: Top level resource folder of the container.
* ``public_folder``: Folder to serve php files from (volume).
* ``private_folder``: Password protected folder to serve php files from (volume).
* ``http_port``: *HTTP* port that is mapped to your local system.
* ``https_port``: *HTTPS* port that is mapped to your local system.

You can also specify these options by using environment variables. The command ``car env php`` explains their corresponding usage:

```console
[qtc@devbox ~]$ car env php
[+] Available environment variables are:
[+] 
[+] Name                   Current Value                     Description
[+] car_http_port          127.0.0.1:80                      HTTP port that is mapped to your local system.
[+] car_https_port         127.0.0.1:443                     HTTPS port that is mapped to your local system.
[+] car_public_folder      /home/qtc/arsenal/php/public      Folder to serve php files from (volume).
[+] car_private_folder     /home/qtc/arsenal/php/private     Password protected folder to serve php files from (volume).
[+] car_local_uid          1000                              UID of the nginx user.
```
