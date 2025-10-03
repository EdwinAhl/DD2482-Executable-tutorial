# A secure solution Part 1 - Setting up OpenBao
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
`docker exec -it openbao` to send commands as if you where inside of the container.

```bash
sudo docker exec -it openbao bao login root
```{{exec}}
- `sudo` this is for managing privledged process as root
- `docker` program we are targetting
- `exec` for executing commands in containers
- `-i` for interactive
- `-t` for a pseudo-tty which displays the result of executed command as if inside the container.
- `openbao` this is the name of the running container that docker recognizes (see previous command)

This command will:
- Authenticate you as root and give you permissions as root by supplying the token "root" to the server for running commands with highest privileges.
- Sets the environment variable (inside the container) VAULT_TOKEN to "root" for simplifying future access to the OpenBao server instance with the "bao" command
- Do note that "root" is a static token for root access and should not be used in production.

## What would a production instance look like?
Remember that we mentioned earlier about a special algorithm called Shamir Secret Sharing? That is part of OpenBaos functionality in production. By leveraging the use of multiple user to generate a key, means that without those people the server remain sealed and inaccessible. The bigger thing is that the produciton server requires you to start the instance with `bao operator init` which creates the aforementioned unseal key and a root token that is mainly used in cohesion with auth methods (OIDC, LDAP, etc)

Main differences to OpenBao in prodcution can be outlined in the following way:
- in-memory storage switches to dedicated backend such as PostgreSQL on dedicated hardware (SSD, HDD) with potnetial for High-availbility clustering and replication
- Networking utilize HTTPS instead HTTP
- atleast one audit devices will be configured (syslog or file)

