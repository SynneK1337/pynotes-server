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
        self.cursor = self.database.cursor()

        # Create tables if not exists
        self.execute_query(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
            "title VARCHAR(255) NOT NULL, "
            "creation_date datetime NOT NULL, "
            "author_id INT UNSIGNED NOT NULL, "
            "content TEXT)", None
        )

    def execute_query(self, query, data):
        try:
            self.cursor.execute(query, data)
        except mysql.connector.Error as err:
            print(err)
        else:
            self.database.commit()

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

        self.execute_query(query, data)

    def get_notes_list(self, author_id):
        query = (
            "SELECT id, title, creation_date, content "
            "FROM notes WHERE author_id = %s"
        )
        data = (author_id,)
        self.execute_query(query, data)
        notes = []
        for (id, title, creation_date, content) in self.cursor:
            notes.append(
                {
                    "id":               id,
                    "title":            title,
                    "creation_date":    creation_date,
                    "content":          content
                }
            )
        return notes

    def get_note(self, id):
        query = ("SELECT title, creation_date, content FROM notes where id=%s")
        data = (id,)
        self.execute_query(query, data)
        for (title, creation_date, content) in self.cursor:
            return {
                "title":            title,
                "creation_date":    creation_date,
                "content":          content
            }

