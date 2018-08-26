import queue
import random
import sqlite3
import string
import threading


class SQLHandler(object):
    def __init__(self, db):
        self.db = db
        self.insert_queue = queue.Queue(1)
        self.conn = sqlite3.connect(self.db, check_same_thread=False)

    def uuid(self):
        return ''.join(random.sample(string.ascii_letters, 7))

    def select(self, id, queue):
        queue.put(self.conn.execute("SELECT content FROM messages WHERE id=?", [id]))
        return

    def threaded_select(self, id):
        result = queue.Queue()
        thread = threading.Thread(target=self.select, args=(id, result))
        thread.start()
        thread.join()
        return result.get()

    def insert(self, content):
        uuid = self.uuid()
        while self.threaded_select(uuid).fetchall() != []:
            uuid = self.uuid()
        self.conn.execute("""INSERT INTO messages (id, content) 
                             VALUES (?, ?)""", [uuid, content])
        return uuid

    def threaded_insert(self):
        item = self.insert_queue.get()
        uuid = self.insert(item)
        self.insert_queue.task_done()
        return uuid

    def submit(self, content):
        self.insert_queue.put(content)
        uuid = self.threaded_insert()
        self.conn.commit()
        return uuid
