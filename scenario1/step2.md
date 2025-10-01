# A secure solution
## OpenBao solution
The solution you can deploy right now, is OpenBao. OpenBao is a fork of HashiCrop Vault which is why you may see artifacts where "VAULT" is used instead of "BAO". One important difference to other programs is that OpenBao commuincates over HTTP requests rather then using their own protocol. Therefore, we need to set the BAO_ADDR variable such that each HTTP requests reaches the server. 

Now, we start with setting up and running the docker container for OpenBao with: 
```plain
sudo docker run -d --cap-add=IPC_LOCK -p 8200:8200 --name openbao  -e BAO_ADDR=http://0.0.0.0:8200 openbao/openbao server -dev -dev-root-token-id="root"
```{{exec}}

Let's walk through each flag of the docker command:
- `-d` detached mode, runs the container in the background.
- `--cap-add=IPC_LOCK` this options locks memory for certain processes, this is a safety step suggested by OpenBao.
- `-p 8200:8200` exposes the openbao from the internal docker network to the external host network, which allows access to the container from host network.
- `--name openbao` name of container.
- `-e BAO_ADDR=http://0.0.0.0:8200` this makes the openbao commands run within the container to use this address when issueing commands with HTTP requests.
- `openbao/openbao` container name from provider openbao.
- `server` this is an implicit statement, the container interprets the command as "bao server", which simply starts the server.
- `-dev` indicates to run the server in dev mode for experimentation purposes, much like in this tutorial to faciliate ease of use of OpenBao.
- `-dev-root-token-id="root"` this is only for demo pruposes, production version should not have this or any other `dev` keywords when running the server. This flag assigns a static variable for the token with highest privileges.

After the image is download and the container is running, we can start to run commands in the container. In order to do so, we will use the docker command: 
`docker exec -it openbao` to send commands as if you where inside of the container. `-i` for interactive and `-t` for a pseudo-tty which displays the result of executed command as if inside the container.

```bash
sudo docker exec -it openbao bao login root
```{{exec}}
NOTE!! "root" is a static token for root access and should not be used in production.

This command will:
- Authenticate you as root and give you permissions as root by supplying the token "root" to the server for running commands with highest privileges.
- Sets the environment variable (inside the container) VAULT_TOKEN to "root" for simplifying future access to the OpenBao server instance with the "bao" command

## Storing the MySQL password in OpenBao
This will store the password as a key-value (kv) in a secret folder called "foo", with the key "pswd":
```bash
sudo docker exec -it openbao bao kv put -mount=secret foo pswd=S3cret
```{{exec}}


## Create a temporary token for accessing the password 
What we will do next is create a token that only allows reading a folder in OpenBao's Key-Value database called "secret".

To do this we have to make a policy that we then apply to the token. This policy is kept in PolicyForPythonToken.hcl:
```bash
cat PolicyForPythonToken.hcl
```{{exec}}

The language used to specify policies is part of OpenBao's specifiaction and can be customized for your specific needs, but here we will be satsifed with the policy file mentioned above.

Let's move this policy into the container:
```plain
docker cp PolicyForPythonToken.hcl openbao:/root/
```{{exec}}

With the policy inside the container, we now add it by writing the policy to OpenBao:
```plain
sudo docker exec -it openbao bao policy write python-program /root/PolicyForPythonToken.hcl
```{{exec}}

You are almost there! The final step is to now create the token using this newly created policy:
```plain
sudo docker exec -it openbao bao token create -policy="python-program" -ttl=1h -explicit-max-ttl=24h
```{{exec}}

Now you should see lots of information, but for now, copy the text after "token":
```plain
Key                  Value
---                  -----
token                <copy this>
...                  ...
```


## Updating the Python program to use OpenBao
Instead of storing the secret in plaintext, we can now use the OpenBao container that we have setup. We do this by utilizing the OpenBao HTTP API by crafting a request to the server where we authenticate by inputting the token and requesting the database password. We still use the same MySQL connector, but `get_secret` has beeen updated: 

```python
OPENBAO_URL = "http://127.0.0.1:8200" 
MOUNT = "secret"
SECRET_PATH = "foo"
FIELD = "pswd"
TOKEN = input("Token: ")

def get_secret():
    headers = {"X-Vault-Token": TOKEN}
    url = f"{OPENBAO_URL}/v1/{MOUNT}/data/{SECRET_PATH}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["data"][FIELD]
```

Now we can verify this by running the command below and inputting the value for `token` from the previous commmand:
```plain
python openbao.py
```{{exec}}

We get the same result as before, but more secure!
