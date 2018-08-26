import sqlite3

conn = sqlite3.connect("messages.db")

conn.execute("""CREATE TABLE messages
                (
                id varchar(7),
                content varchar(255)
                );""")