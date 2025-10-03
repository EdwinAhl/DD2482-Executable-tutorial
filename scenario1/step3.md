# A secure solution Part 1 - OpenBao Setup
## Setting up OpenBao
The solution you can deploy right now, is OpenBao. OpenBao is a fork of HashiCrop Vault which is why you may see artifacts where "VAULT" is used instead of "BAO". One important difference to other programs is that OpenBao commuincates over HTTP requests rather then using their own protocol. Therefore, we need to set the BAO_ADDR variable such that each HTTP requests reaches the server. 

Now, we start with setting up and running the Docker container for OpenBao with: 
```plain
sudo docker run -d --cap-add=IPC_LOCK -p 8200:8200 --name openbao  -e BAO_ADDR=http://0.0.0.0:8200 openbao/openbao server -dev -dev-root-token-id="root"
```{{exec}}
- `-d` detached mode, runs the container in the background.
- `--cap-add=IPC_LOCK` this options locks memory for certain processes, this is a safety step suggested by OpenBao.
- `-p 8200:8200` exposes the OpenBao from the internal Docker network to the external host network, which allows access to the container from host network.
- `--name openbao` name of container.
- `-e BAO_ADDR=http://0.0.0.0:8200` this makes the openbao commands run within the container to use this address when issueing commands with HTTP requests.
- `openbao/openbao` container name from provider openbao.
- `server` this is an implicit statement, the container interprets the command as "bao server", which simply starts the server.
- `-dev` indicates to run the server in dev mode for experimentation purposes, much like in this tutorial to faciliate ease of use of OpenBao.
- `-dev-root-token-id="root"` this is only for demo purposes, production version should not have this or any other `dev` keywords when running the server. This flag assigns a static variable for the token with highest privileges.

Make sure the container is running:
```plain
docker ps
```{{exec}}

We should be able to see that both the MySQL and OpenBao container are running.

Now it is time to login to OpenBao system as root so that we are later able to configure it:
```bash
sudo docker exec -it openbao bao login root
```{{exec}}
- `sudo docker exec` used to run a command inside an already running container
- `-i` for interactive
- `-t` for a pseudo-tty which displays the result of executed command as if inside the container.
- `openbao` this is the name of the running container that docker recognizes (see previous command)
- `bao` is a CLI tool used to commuincate with the OpenBao instance
- `login <token>` authenticate to OpenBao and assign a essential environment variable to <token>
- `root` token for highest privledges

This command will:
- Authenticate you as root and give you permissions as root by supplying the token "root" to the server for running commands with highest privileges.
- Sets the environment variable (inside the container) VAULT_TOKEN to "root" for simplifying future access to the OpenBao server instance with the "bao" command
- Do note that "root" is a static token for root access and should not be used in production.

## What would a production instance look like?
Remember that we mentioned earlier about a special algorithm called Shamir Secret Sharing? That is part of OpenBao's functionality in production. By leveraging the use of multiple user to generate a key, means that without those people the server remain sealed and inaccessible. The bigger thing is that the produciton server requires you to start the instance with `bao operator init` which creates the aforementioned unseal key and a root token that is mainly used in cohesion with other services such as auth methods (OIDC, LDAP, etc)

Main differences to OpenBao in prodcution can be outlined in the following way:
- In-memory storage switches to a dedicated backend such as PostgreSQL on dedicated hardware (SSD, HDD) with support for High-availability clustering and replication
- Networking utilize HTTPS instead HTTP
- Atleast one audit devices needs to be configured (syslog or file)

