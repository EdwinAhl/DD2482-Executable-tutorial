## Setup Database
'sudo docker run -d --name demo-db  -e MYSQL_ROOT_PASSWORD=S3cret -p 3306:3306 mysql:8'{{exec}}

Wait 15 seconds else error

'sudo docker exec -i demo-db mysql -u root -pS3cret < db.sql'{{exec}}


## Setup Python Virtual Environment
'sudo apt install python3 python3-venv python3-pip -y'{{exec}}

'python3 -m venv venv'{{exec}}

'source venv/bin/activate'{{exec}}


## Run plaintext.py to connect to database and show all users
'pip install mysql-connector-python'{{exec}}

'python plaintext.py'{{exec}}


## Use detect-secrets to find plaintext secrets in plaintext.py
'pip install detect-secrets'{{exec}}

'detect-secrets scan program.py'{{exec}}

