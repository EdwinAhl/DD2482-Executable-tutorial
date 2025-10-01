# An insecure solution
## Setup Database
To start, we need to setup a secure database. The command below creates a MySQL docker container secured by the username `root` and password `S3cret`.
```plain
sudo docker run -d --name demo-db -e MYSQL_ROOT_PASSWORD=S3cret -p 3306:3306 mysql:8; sleep 15
```{{exec}}

This command takes a while and we need to wait at least 15 seconds between running the command above and below, in the meanwhile, enjoy this riveting gameplay:

![minecraft parkour gif](./assets/minecraft-tas.gif)

Now that we have a MySQL docker container running , we can import a pre-made database: 
```plain
sudo docker exec -i demo-db mysql -u root -pS3cret < db.sql
```{{exec}}

Great! Now we have a database with secured data!

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

Use the environment:
```plain
source venv/bin/activate
```{{exec}}


## Connect to the database and show all users using python
Before running the python program, we need the pip module `mysql-connector` which we use to connect to the database:  
```plain
pip install mysql-connector-python
```{{exec}}

Now we can finally run the program:
```plain
python plaintext.py
```{{exec}}


## Use detect-secrets to find plaintext secrets
It works! But how? As the name might give away, the password could be written in plaintext. 
Let's investigate this using the pip module `detect-secrets`:
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

Here we can clearly see that the program connects to the mysql database by inputting in plaintext the username and password. This is insecure and must be fixed, but how?
