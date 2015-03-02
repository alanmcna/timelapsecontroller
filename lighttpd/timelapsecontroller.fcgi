#!/usr/bin/python
#: optional path to your local python site-packages folder
#import sys
#sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')

from flup.server.fcgi import WSGIServer
from timelapsecontroller import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = 'index.py'
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run('0.0.0.0')
