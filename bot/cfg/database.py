import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # ЗАПРОСЫ К ТАБЛИЦЕ CONFIG
    def get_all_config(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM config").fetchone()

    def add_user(self, user_id):
        with self.connection:
            all_user = self.cursor.execute("SELECT * FROM config").fetchone()[3].split(",")
            if user_id not in all_user:
                return self.cursor.execute("UPDATE config SET USERS = USERS || ? WHERE ID = 1", (f"{user_id},",))

    def del_user(self, user_id: str):
        with self.connection:
            all_user = self.cursor.execute("SELECT * FROM config").fetchone()[3].split(",")
            if user_id in all_user:
                all_user.remove(user_id)
                return self.cursor.execute("UPDATE config SET USERS = ? WHERE ID = 1", (",".join(all_user),))

    def get_all_file(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM file").fetchall()

    def add_file(self, file_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `file` (`file_name`) VALUES (?)", (str(file_name),))

    def done_file(self, file_id):
        with self.connection:
            return self.cursor.execute("UPDATE file SET done = 1 WHERE ID = ?", (file_id,))
