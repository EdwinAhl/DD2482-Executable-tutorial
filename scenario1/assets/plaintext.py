import mysql.connector

def get_secret():
    password = "S3cret"
    return password

def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=get_secret(),
        database="db"
    )

def main():
    print("Getting users using plaintext password ...")
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
