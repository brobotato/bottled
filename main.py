import os.path
import queue
import random
import sqlite3
import string
import threading

import cherrypy


class Bottled(object):

    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def create(self):
        return open('create.html')

    @cherrypy.expose
    def message(self, id = 'defaultid'):
        if handler.threaded_select(id).fetchall() != []:
            return handler.threaded_select(id).fetchone()
        else:
            return open('index.html')


@cherrypy.expose
class BottledRequests(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, text):
        handler.submit(text)

    def DELETE(self):
        pass


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
        self.conn.execute('''INSERT INTO messages (id, content) 
                             VALUES (?, ?)''', [uuid, content])

    def threaded_insert(self):
        item = self.insert_queue.get()
        self.insert(item)
        self.insert_queue.task_done()

    def submit(self, content):
        self.insert_queue.put(content)
        thread = threading.Thread(target=self.threaded_insert())
        thread.start()
        thread.join()
        self.conn.commit()


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/submit': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    db = 'messages.db'
    handler = SQLHandler(db)

    webapp = Bottled()
    webapp.submit = BottledRequests()
    cherrypy.quickstart(webapp, '/', conf)
