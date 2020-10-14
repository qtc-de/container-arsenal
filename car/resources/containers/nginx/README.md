### nginx

----

The *nginx* container starts a *nginx* webserver that maps an *HTTP* and an *HTTPS* port to your local system. 
Beside providing an easy way for file downloads, the server has also a directory with *WebDav* enabled,
which can be used for file uploads.

To offer files for a download, just place them in the ``download`` resource folder of the container (e.g.
``~/arsenal/nginx/download`` and they will be accessible within the *webroot* of the *HTTP* server. To upload
files, you have to use the *PUT* method on the ``/uploads`` endpoint. Your files will be saved inside the
``upload`` resource folder (e.g. ``~/arsenal/nginx/upload``). Access to the upload folder of the webserver
is only allowed with valid credentials that are randomly generated during the container startup.


### Example Usage

----

In the following you find a demonstration of an example usage. First of all, the *nginx* container is started:

```console
[qtc@kali ~]$ car run nginx 
[+] Environment Variables:
[+]	car_nginx_folder              /home/qtc/arsenal/nginx
[+]	car_download_folder           /home/qtc/arsenal/nginx/download
[+]	car_upload_folder             /home/qtc/arsenal/nginx/upload
[+]	car_http_port                 80
[+]	car_https_port                443
[+] 
[+] Running: sudo -E docker-compose up
Recreating car.nginx ... done
Attaching to car.nginx
car.nginx    | [+] No password was specified.
car.nginx    | [+] Generated random password: FTmnkR6K
car.nginx    | [+] Creating .htpasswd file.
car.nginx    | [+] WebDAV access allowed for default:FTmnkR6K
car.nginx    | [+] Adjusting volume permissions.
car.nginx    | [+] Starting nginx daemon.
```

Now, an example file is placed within the ``~/arsenal/nginx/download`` folder and it is demonstrated that it can be
accessed from whe *webroot* of the webserver.

```console
[qtc@kali ~]$ echo "Hello World :D" > ~/arsenal/nginx/download/hello.txt
[qtc@kali ~]$ curl 127.0.0.1/hello.txt
Hello World :D
[qtc@kali ~]$ curl -k https://127.0.0.1/hello.txt
Hello World :D
```

Next, an example file is uploaded by using *WebDAV* access and it is demonstrated that the corresponding file can then
be found within the ``~/arsenal/nginx/upload`` folder.

```console
[qtc@kali ~]$ echo "Hi World :)" > hi.txt
[qtc@kali ~]$ curl -X PUT http://default:FTmnkR6K@127.0.0.1/upload/hi.txt -d @hi.txt 
[qtc@kali ~]$ cat ~/arsenal/nginx/upload/hi.txt 
Hi World :)
```


### Configuration Options

----

The following configuration options can be adjusted within your ``car.toml`` configuration file:

* ``nginx_folder``: Top level resource folder of the container.
* ``upload_folder``: Upload resource folder of the container (volume).
* ``download_folder``: Download resource folder of the container (volume).
* ``http_port``: *HTTP* port that is mapped to your local system.
* ``https_port``: *HTTPS* port that is mapped to your local system.

You can also specify these options by using environment variables. The command ``car env nginx`` explains their corresponding usage:

```console
[qtc@kali ~]$ car env nginx 
[+] Available environment variables are:
[+] Name                    Current Value                              Description
[+] car_http_port           80                                         HTTP port that is mapped to your local system.
[+] car_https_port          443                                        HTTPS port that is mapped to your local system.
[+] car_upload_folder       /home/qtc/arsenal/nginx/upload             Upload resource folder of the container (volume).
[+] car_download_folder     /home/qtc/arsenal/nginx/download           Download resource folder of the container (volume).
```
