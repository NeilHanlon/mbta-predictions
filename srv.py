import sys
reload(sys)
sys.setdefaultencoding("utf8")
from copy import copy

from gevent import monkey; monkey.patch_all()
import gevent
import gevent.wsgi

from app import theApp

SERVER_PORT = 80


http_server = gevent.wsgi.WSGIServer(('', SERVER_PORT), theApp)
http_server.serve_forever()
