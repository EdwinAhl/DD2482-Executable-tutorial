# An insecure solution
## Setup Database
To start, we need to setup a secure database. The command below creates a mysql docker container secured by the username `root` and password `S3cret`.
```plain
sudo docker run -d --name demo-db -e MYSQL_ROOT_PASSWORD=S3cret -p 3306:3306 mysql:8; sleep 10
```{{exec}}

**IMPORTANT: Wait at least 10-15 seconds between running the command above and below!**
Otherwise the command below will generate an error and you will have to run it again, that is why we have a `sleep 10` at the end of the first command.

Now that we have a container running mysql, we can import a pre-made database from *db.sql*: 
```plain
sudo docker exec -i demo-db mysql -u root -pS3cret < db.sql
```{{exec}}

Great, now we have a database with secured data!

## Setup Python Virtual Environment
To run a python program that connects to the database and retrieves data, we first setup a python virtual envionment to make the rest of the setup easier.

Install the environment:
```plain
sudo apt install python3 python3-venv python3-pip -y
```{{exec}}

Create the environment:
```plain
python3 -m venv venv
```{{exec}}

And use the environment:
```plain
source venv/bin/activate
```{{exec}}


## Run plaintext.py to connect to database and show all users
Before running the python program, we need mysql-connector which we use to connect to the database:  
```plain
pip install mysql-connector-python
```{{exec}}

Now we can finally run the program:
```plain
python plaintext.py
```{{exec}}


## Use detect-secrets to find plaintext secrets in plaintext.py
It works! But how? As the name might give away, the password could be written in plaintext. 
Let's investigate this using the pip module detect-secrets:
```plain
pip install detect-secrets
```{{exec}}

```plain
detect-secrets scan plaintext.py
```{{exec}}

It shows a vulnerability on line 4, let's examine further:

```plain
cat plaintext.py -n
```{{exec}}

Here we can clearly see that the program connects to the mysql database by inputting in plaintext the username and password. This is outragous and must be fixed, but how?
