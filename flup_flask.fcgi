from flup.server.fcgi import WSGIServer
from dark_soul import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/tmp/flask_fastcgi.sock').run()
