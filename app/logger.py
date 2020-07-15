import pika
import pika.exceptions
import os

EXCHANGE = 'calc_logs'


class Logger:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
            cls.instance.connections = dict()
            cls.instance.channels = dict()
        return cls.instance

    def channel(self):
        pid = os.getpid()
        if pid not in self.connections or pid not in self.channels or self.connections[pid] is None:
            self.connections[pid] = pika.BlockingConnection(
                pika.ConnectionParameters('localhost')
            )
            self.channels[pid] = self.connections[pid].channel()
            self.channels[pid].exchange_declare(
                exchange=EXCHANGE,
                exchange_type='direct'
            )
        return self.channels[pid]

    def write(self, tag='LOG', msg=''):
        try:
            self.channel().basic_publish(exchange=EXCHANGE, routing_key=tag, body=msg)
        except (pika.exceptions.StreamLostError, pika.exceptions.ChannelWrongStateError):
            if self.connections[os.getpid()].is_open:
                self.connections[os.getpid()].close()
            self.connections[os.getpid()] = None
            try:
                self.channel().basic_publish(exchange=EXCHANGE, routing_key=tag, body=msg)
            except (pika.exceptions.StreamLostError, pika.exceptions.ChannelWrongStateError):
                pass

    def log(self, msg='None'):
        self.write('LOG', msg)

    def debug(self, msg=''):
        self.write('DEBUG', msg)

    def error(self, msg=''):
        self.write('ERROR', msg)

    def __del__(self):
        self.log('Stop logger')
        for connection in self.connections.values():
            connection.close()
