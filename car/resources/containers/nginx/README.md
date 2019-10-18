## nginx

This container does simply start a nginx server that exposes HTTP and HTTPS ports on your local system. 
Beside providing easy file downloads, the server has also a directory there WebDav is configured. This
enables you to easily upload files via HTTP/S.

To download files, just place them in the ``download`` resource folder of the container. They will be
accessible without any subfolder over the HTTP server. To upload files, you have to use the PUT method
on the ``/uploads`` endpoint. Your files will be saved inside the ``upload`` resource folder. The password
for the WebDav folder is generated randomly on container startup.

## Configuration Options

* nginx_folder: Top level resource folder of the container.
* download_folder: Download resource folder of the container.
* upload_folder: Upload resource folder of the container.
* http_port: HTTP port that is exposed on your local host.
* https_port: HTTPS port that is exposed on your local host.
