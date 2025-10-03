# A Secure Solution Part 2 - Using Python
## Storing the MySQL password in OpenBao
Let´s start with the following command which will store the password as a key-value (kv) in a secret folder called `foo`, with the key `pswd` and value `S3cret`:
```bash
sudo docker exec -it openbao bao kv put -mount=secret foo pswd=S3cret
```{{exec}}
- `bao` is a CLI tool used to communicate with the OpenBao instance
- `kv` targets the Key-Value secrets engine
- `put` adds or updates new information
- `-mount=secret` specifies the KV engine mount point to `/secret`
- `foo` assigns the top-level key as `foo` (think of it like a folder or namespace)
- `pswd=S3cret` is the actual data being stored as a key-value pair

To simplify, you can *imagine* the data saved as a JSON file:
```json
{
  "secret": {
    "foo": {
      "pswd": "S3cret"
    }
  }
}  
```

## Create a temporary token for accessing the password 
What we will do next is create a token that only allows reading the special mount point `secret` in the OpenBao system, where we stored the password.

To do this we have to make a policy that we then apply to the token. This policy is kept in `PolicyForPythonToken.hcl`:
```bash
cat PolicyForPythonToken.hcl
```{{exec}}

The language used to specify policies is part of OpenBao's specification and can be customized for your specific needs, but here we will be satisfied with the policy file mentioned above.

Let's move this policy into the container:
```plain
docker cp PolicyForPythonToken.hcl openbao:/root/
```{{exec}}

With the policy inside the container, we now add it by writing the policy to OpenBao and calling it "python-program":
```plain
sudo docker exec -it openbao bao policy write python-program /root/PolicyForPythonToken.hcl
```{{exec}}
- `bao` is a CLI tool used to communicate with the OpenBao instance
- `policy` to target policy management of OpenBao
- `write` means creating a new policy
- `python-program` name for the policy
- `/root/PolicyForPythonToken.hcl` path to the policy file formatted for OpenBao

You are almost there! The final step is to now create the OpenBao access token using this newly created policy and save it as a shell variable:
```plain
TOKEN=$(sudo docker exec -i openbao bao token create -policy="python-program" -ttl=1h -explicit-max-ttl=24h | awk '/^token[[:space:]]/{print $2}')
```{{exec}}
- `TOKEN=$(...)` assigns a shell variable as the output from the command inside the parentheses
- `token create` instructs `bao` to create a new token
- `-policy="python-program"` assign the token the policy "python-program" (created before)
- `-ttl=1h` set the token's Time To Live to 1 hour
- `-explicit-max-ttl=24h` sets the maximum allowed lifetime the token can ever be renewed to 24 hours 
- `| awk '/^token[[:space:]]/{print $2}'` pipes the output to awk that matches the line starting with "token " and prints the second whitespace-separated field (token value)

## Updating the Python program to use OpenBao
Instead of storing the secret in plaintext, we can now use the OpenBao container that we have set up. We do this by utilizing the OpenBao HTTP API by crafting a request to the server where we authenticate by inputting the token and requesting the database password. We still use the same MySQL connector, but `get_secret` has been updated: 

```python
OPENBAO_URL = "http://127.0.0.1:8200" 
MOUNT = "secret"
PATH = "foo"
FIELD = "pswd"
TOKEN = sys.argv[1]

def get_secret():
    headers = {"X-Vault-Token": TOKEN}
    url = f"{OPENBAO_URL}/v1/{MOUNT}/data/{SECRET_PATH}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["data"][FIELD]
```
We can check if `detect-secrets` finds anything in this file:
```plain
detect-secrets scan openbao.py
```{{exec}}

We should get an empty result like this: `"results": {}`

Now we can finally verify the OpenBao solution by running the command below, and authenticating using the value of `"$TOKEN"` from the previous command:
```plain
python openbao.py "$TOKEN"
```{{exec}}

We get the same result as before, but more secure!
