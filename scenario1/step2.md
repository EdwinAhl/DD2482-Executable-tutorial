## Lightly introduce OpenBao and how it works in production

```plain
sudo docker run -d --cap-add=IPC_LOCK -p 8200:8200 --name openbao  -e BAO_ADDR=http://0.0.0.0:8200 openbao/openbao server -dev -dev-root-token-id="root"
```{{exec}}

Let's walk through each flag of the docker command:
- ```-d``` detached mode, runs the container in the background
- 

## For 