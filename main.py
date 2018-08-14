import os.path
from sqlhandler import SQLHandler

import cherrypy


class Bottled(object):

    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def create(self):
        return open('create.html')

    @cherrypy.expose
    def message(self, id='defaultid'):
        if handler.threaded_select(id).fetchall() != []:
            return handler.threaded_select(id).fetchone()
        else:
            return open('index.html')


@cherrypy.expose
class BottledRequests(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, text):
        uuid = handler.submit(text)
        return uuid

    def DELETE(self):
        pass


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
