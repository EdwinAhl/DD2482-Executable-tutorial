# An Insecure Solution Part 2 - Using Python
## Setup a Python virtual environment
To run a Python program that connects to the MySQL database and retrieves data, we first set up a Python virtual environment to make the rest of the setup easier.

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

We should now be able to see `(venv)` at the beginning of the shell prompt, indicating that the Python virtual environment is active and any Python commands or packages will use this environment

## Connect to the database and show all users using Python
Before running the Python program, we need the pip module `mysql-connector`, which we use to connect to the database:  
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

Here we can clearly see that the program connects to the MySQL database by inputting, in plaintext, the username and password. This is insecure and must be fixed, but how?