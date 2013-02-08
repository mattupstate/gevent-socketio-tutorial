
from gevent import monkey; monkey.patch_all();
from socketio.server import SocketIOServer

from app import app

server = SocketIOServer(('0.0.0.0', 5000), app, resource="socket.io")

if __name__ == '__main__':
    print 'Running server'
    server.serve_forever()
