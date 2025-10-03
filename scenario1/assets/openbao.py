import mysql.connector
import requests
import sys

OPENBAO_URL = "http://127.0.0.1:8200" 
MOUNT = "secret"
PATH = "foo"
FIELD = "pswd"
TOKEN = sys.argv[1]

def get_secret():
    headers = {"X-Vault-Token": TOKEN}
    url = f"{OPENBAO_URL}/v1/{MOUNT}/data/{PATH}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["data"][FIELD]


def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=get_secret(),
        database="db"
    )

def main():
    print("Getting users using OpenBao ...")
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    print("User Firstname Lastname")
    for r in rows:
        print(r)
    cursor.close()
    conn.close()
   
if __name__ == "__main__":
    main()   
