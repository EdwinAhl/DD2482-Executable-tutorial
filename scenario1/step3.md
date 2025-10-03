# A secure solution Part 1 - OpenBao Setup
## Setting up OpenBao
The solution you can deploy right now is OpenBao. OpenBao is a fork of HashiCorp Vault, which is why you may see artifacts where "VAULT" is used instead of "BAO". One important difference to other programs is that OpenBao communicates over HTTP requests rather than using its own protocol. Therefore, we need to set the BAO_ADDR variable such that each HTTP request reaches the server. 

Now, we start with setting up and running the Docker container for OpenBao with: 
```plain
sudo docker run -d --cap-add=IPC_LOCK -p 8200:8200 --name openbao  -e BAO_ADDR=http://0.0.0.0:8200 openbao/openbao server -dev -dev-root-token-id="root"
```{{exec}}
- `-d` detached mode, runs the container in the background
- `--cap-add=IPC_LOCK` this option locks memory for certain processes, this is a safety step suggested by OpenBao
- `-p 8200:8200` exposes the OpenBao from the internal Docker network to the external host network, which allows access to the container from the host network.
- `--name openbao` name of container
- `-e BAO_ADDR=http://0.0.0.0:8200` this makes the openbao commands run within the container to use this address when issuing commands with HTTP requests
- `openbao/openbao` container name from provider openbao.
- `server` this is an implicit statement, the container interprets the command as "bao server", which simply starts the server
- `-dev` indicates to run the server in dev mode for experimentation purposes, much like in this tutorial to facilitate ease-of-use of OpenBao
- `-dev-root-token-id="root"` this is only for demo purposes, production version should not have this or any other `dev` keywords when running the server. This flag assigns a static variable for the token with the highest privileges

Make sure the container is running:
```plain
docker ps
```{{exec}}

We should be able to see that both the MySQL and OpenBao containers are running.

Now it is time to log in to the OpenBao system as root so that we are later able to configure it:
```bash
sudo docker exec -it openbao bao login root
```{{exec}}
- `sudo docker exec` used to run a command inside an already running container
- `-i` for interactive
- `-t` for a pseudo-tty which displays the result of executed command as if inside the container.
- `openbao` this is the name of the running container that Docker recognizes (see previous command)
- `bao` is a CLI tool used to communicate with the OpenBao instance
- `login <token>` authenticate to OpenBao and assign an essential environment variable to \<token\>
- `root` token for highest privileges

This command will:
- Authenticate you as root and give you permissions as root by supplying the token "root" to the server for running commands with the highest privileges.
- Sets the environment variable (inside the container) VAULT_TOKEN to "root" for simplifying future access to the OpenBao server instance with the "bao" command
- Do note that "root" is a static token for root access and should not be used in production.

## What would a production instance look like?
Remember that we mentioned earlier about a special algorithm called Shamir Secret Sharing? That is part of OpenBao's functionality in production. By leveraging the use of multiple users to generate a key, the OpenBao instance remains sealed and inaccessible if not enough keys are present, meaning e.g. key leakage is less severe. The bigger thing is that the production server requires you to start the instance with `bao operator init`, which creates the aforementioned unseal key and a root token that is mainly used in conjunction with other services such as auth methods (OIDC, LDAP, etc)

Main differences to OpenBao in production can be outlined in the following way:
- In-memory storage switches to a dedicated backend such as PostgreSQL on dedicated hardware (SSD, HDD) with support for High-availability clustering and replication
- Networking utilizes HTTPS instead of HTTP
- At least one audit device needs to be configured (syslog or file)

