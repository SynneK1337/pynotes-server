import mysql.connector
from mysql.connector import errorcode


class Database():
    def __init__(self, host, user, passwd, db):
        try:
            self.database = mysql.connector.connect(
                host=host,
                password=passwd,
                user=user,
                database=db,
                auth_plugin="mysql_native_password"
            )
        except mysql.connector.Error as err:
            print(err)
        self._cursor = self.database.cursor()

    def _execute_query(self, query, data):
        try:
            self._cursor.execute(query, data)
        except mysql.connector.Error as err:
            print(err)
        else:
            try:
                self.database.commit()
            except mysql.connector.Error as err:
                print(err)

    def create_note(self, title, creation_date, author_id, content):
        query = (
            "INSERT INTO notes "
            "VALUES (%(id)s, %(title)s, %(creation_date)s, "
            "%(author_id)s, %(content)s)"
        )

        data = {
            "id":               None,
            "title":            title,
            "creation_date":    creation_date,
            "author_id":        author_id,
            "content":          content
        }

        self._execute_query(query, data)

    def get_notes_list(self, user_id):
        query = (
            "SELECT id, title, creation_date "
            "FROM notes WHERE user_id = %s"
        )
        data = (user_id,)
        self._execute_query(query, data)
        notes = []
        for (id, title, creation_date) in self._cursor:
            notes.append(
                {
                    "id":               id,
                    "title":            title,
                    "creation_date":    creation_date,
                }
            )
        return notes

    def get_note(self, note_id, user_id):
        query = (
            "SELECT title, creation_date, content FROM notes "
            "WHERE id=%(note_id)s AND user_id=%(user_id)s"
        )
        data = {
                "note_id": note_id,
                "user_id": user_id
        }

        self._execute_query(query, data)
        for (title, creation_date, content) in self._cursor:
            return {

                "title":            title,
                "creation_date":    creation_date,
                "content":          content
            }

    def register(self, username, password):
        query = (
            "INSERT INTO accounts "
            "VALUES(NULL, %(username)s, %(password)s)"
        )
        data = {
            "username": username,
            "password": password
        }
        try:
            self._execute_query(query, data)

        except mysql.connector.Error:
            return False

        else:
            return True

    def login(self, username, password):
        self.remove_token_by_user_id(self.get_user_id(username))

        query = (
            "SELECT EXISTS(SELECT 1 FROM accounts WHERE "
            "username=%(username)s AND password=%(password)s)"
        )
        data = {
            "username": username,
            "password": password
        }

        self._execute_query(query, data)
        return (1,) in self._cursor

    def get_user_id(self, username):
        query = (
            "SELECT id FROM accounts WHERE username=%(username)s"
        )
        data = {"username": username}

        self._execute_query(query, data)
        for id in self._cursor:
            return int(id[0])

    def add_token(self, user_id, token, expiration_date):
        query = (
            "INSERT INTO tokens "
            "VALUES(%(user_id)s, %(token)s, %(expiration_date)s)"
        )
        data = {
            "user_id":          user_id,
            "token":            token,
            "expiration_date":  expiration_date
        }

        self._execute_query(query, data)

    def remove_token_by_user_id(self, user_id):
        query = ("DELETE FROM tokens WHERE user_id=%(user_id)s")
        data = {"user_id": user_id}

        self._execute_query(query, data)

    def remove_token(self, token):
        query = (
            "DELETE FROM tokens WHERE token=%(token)s"
        )
        data = {
            "token": token
        }

        self._execute_query(query, data)

    def get_token_expiration_date(self, token):
        query = (
            "SELECT expiration_date FROM tokens "
            "WHERE token=%(token)s"
        )
        data = {"token": token}

        self._execute_query(query, data)

        for expiration_date in self._cursor:
            return expiration_date[0]

    def remove_note(self, note_id, user_id):
        query = (
            "DELETE FROM notes WHERE "
            "id=%(note_id)s AND user_id=%(user_id)s"
        )
        data = {
            "note_id": note_id,
            "user_id": user_id
        }

        self._execute_query(query, data)

    def modify_note(self, note_id, user_id, title, content):
        query = (
            "UPDATE notes SET title=%(title)s, content=%(content)s "
            "WHERE id=%(note_id)s AND user_id=%(user_id)s"
        )
        data = {
            "note_id":  note_id,
            "user_id":  user_id,
            "title":    title,
            "content":  content
        }

        self._execute_query(query, data)

if __name__ == "__main__":
    from datetime import datetime
    db = Database("localhost", "root", "3dSynN3K", "pynotes")
    db.login("synnek", "3dSynN3K")
