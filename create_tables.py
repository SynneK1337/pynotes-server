import mysql.connector

if __name__ == "__main__":
    print("[i] Connecting to database...")

    # Connecting to database
    # Edit lines below
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='password',
            host='127.0.0.1',
        )

    except mysql.connector.Error as err:
        print(f"[-] {err}")

    else:
        cursor = cnx.cursor()
        print("[+] Connected successful")

    # Creating database
    print("[i] Creating database pynotes")
    try:
        cursor.execute(
            "CREATE DATABASE pynotes DEFAULT CHARACTER SET 'utf8'"
        )

    except mysql.connector.Error as err:
        print(f"[-] {err}")

    else:
        cursor.execute("USE pynotes")
        print("[+] Database created successful")

    # Tables definitions

    tables = {}

    tables["notes"] = (
        "CREATE TABLE notes ("
        "id int unsigned primary key auto_increment, "
        "title varchar(255), "
        "creation_date datetime, "
        "user_id int unsigned, "
        "content text)"
    )

    tables["accounts"] = (
        "CREATE TABLE accounts ("
        "id int unsigned auto_increment, "
        "username varchar(32), "
        "password varchar(255), "
        "primary key(id, username))"
    )

    tables["tokens"] = (
        "CREATE TABLE tokens ("
        "user_id int unsigned primary key, "
        "token varchar(255), "
        "expiration_date datetime)"
    )

    # Creating tables
    for table in tables:
        print(f"[i] Creating table {table}...")
        try:
            cursor.execute(tables[table])

        except mysql.connector.Error as err:
            print(f"[-] {err}")

        else:
            print(f"[+] table {table} created successful.")

    print("[+] All tables created sucessfully.")
    cnx.close()
