## ftp

The ftp container does simply launch a vsftpd server and makes it accessible through your host system. 
The Server can be accessed either anonymously or with credentials. Depending on the used login credentials, 
the uploaded / provided files are located in a different folder. 

## Configuration Options

* ftp_folder: This is the top level resource folder of the container.
* anon_folder: This is the resource folder that is used for anonymous user uploads.
* user_folder: This is the resource folder that is used for authenticated uploads.
* ftp_port: The port where the FTP server is listening.



