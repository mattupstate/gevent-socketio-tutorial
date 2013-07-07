
import time

from celery import Celery
from flask import Flask, render_template, request, flash
from redis import StrictRedis
from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from assets import assets
import config

redis = StrictRedis(host=config.REDIS_HOST)

celery = Celery(__name__)
celery.config_from_object(config)

app = Flask(__name__)
app.config.from_object(config)
assets.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if redis.llen(config.MESSAGES_KEY):
            flash('Task is already running', 'error')
        else:
            tail.delay()
            flash('Task started', 'info')
    return render_template('index.html')


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    socketio_manage(request.environ, {
        '/tail': TailNamespace
    })
    return app.response_class()


@celery.task
def tail():
    for i in range(0, 20):
        msg = 'Task message %s\n' % i
        redis.rpush(config.MESSAGES_KEY, msg)
        redis.publish(config.CHANNEL_NAME, msg)
        time.sleep(1)
    redis.delete(config.MESSAGES_KEY)


class TailNamespace(BaseNamespace):
    def listener(self):
        # Emit the backlog of messages
        messages = redis.lrange(config.MESSAGES_KEY, 0, -1)
        self.emit(config.SOCKETIO_CHANNEL, ''.join(messages))

        self.pubsub.subscribe(config.CHANNEL_NAME)

        for m in self.pubsub.listen():
            if m['type'] == 'message':
                self.emit(config.SOCKETIO_CHANNEL, m['data'])

    def on_subscribe(self):
        self.pubsub = redis.pubsub()
        self.spawn(self.listener)
