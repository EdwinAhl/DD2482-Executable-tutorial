# An Insecure Solution Part 1 - MySQL Setup
## Setting up a secure database
To start, we need to setup a secure database. The command below creates a MySQL Docker container secured by the username `root` and password `S3cret`.
```plain
sudo docker run -d --name demo-db -e MYSQL_ROOT_PASSWORD=S3cret -p 3306:3306 mysql:8; sleep 15
```{{exec}}
- `sudo docker run` run a new Docker container with root priviliges
- `-d` detached mode, run the container in the background
- `--name demo-db` assigns the container name "demo-db"
- `-e MYSQL_ROOT_PASSWORD=S3cret` set the root password as `S3cret` inside the container 
- `-p 3306:3306` map port 3306 on the host to port 3306 in the container so that we can access MySQL from the host
- `mysql:8` use the Docker image `mysql` version 8
- `; sleep 15` after the previous command has finished, sleep for 15 seconds

This command takes a while to finish and we need to wait at least 15 seconds between running the command above and below, in the meanwhile, in the meantime, enjoy this riveting gameplay:

![minecraft parkour gif](./assets/minecraft-tas.gif)

Make sure the container is running:
```plain
docker ps
```{{exec}}

## Importing database
Now that we have a MySQL Docker container running , we can import a pre-made database: 
```plain
sudo docker exec -i demo-db mysql -u root -pS3cret < db.sql
```{{exec}}
- `docker exec` run a command inside an existing container
- `i` keep STDIN open to send input to the container
- `demo-db` name of the container where the command will run
- `mysql -u root -pS3cret` connect to the MySQL client as user root and use password `S3cret`
- `< db.sql` redirect the contents of `db.sql` into the MySQL command, effectively executing the SQL script in the database

If the command above generates an error (warning is fine), make sure to wait 15 seconds after the first command has finished and then run the command again.

Verify the import with:
```plain
sudo docker exec -i demo-db mysql -u root -pS3cret -e "SHOW DATABASES;"
```{{exec}}

We should be able to see `db` in there.

Great! Now we have a database with secured data!
