## neo4j

Neo4j is a graph database that is required by BloodHound. It is not installed on my base image, 
and every time I need BloodHound I find myself looking for tutorials on how to install it quickly. 
In order to speed up this process, I have created this small container which starts a full working
database on demand.

## Configuration Options
* neo4j_folder: Top level resource folder of neo4j. All database relevant data will be stored here.
* http_port: HTTP port of neo4j that will be exposed on your local system.
* bolt_port: Bolt port of neo4j that will be exposed on your local system.

In contrast to the MySQL container, the password will reset on each database startup and a new randomly
generated one is used. If this is annoying to you, you can change the behavior inside the startup script.
