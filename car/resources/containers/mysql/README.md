## mysql

The mysql container does simply start a mysql server with a root and one low privileged account. 
To be honest, it is not super useful, but sometimes I want to test some queries or try to connect
some remote services with my own database. Therefore, the container can safe some time in very specific
situations.

## Configuration Options

*  mysql_folder: Top level resource folder. All database relevant data is stored here.
*  mysql_port: Port on which the mysql server will be listening on your local system.
*  root_password: Password of the root user account (randomly generated if not specified)
*  user_password: Password of the low privileged user account (randomly generated if not specified)

If you want to add passwords inside the configuration file, you need also to modify the ``docker-compose.yml``
of the container to use these passwords as environment variables. In contrast to the neo4j container, the mysql
passwords will not change then the container is started with a pre-existent mysql database.
