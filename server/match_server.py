#!/usr/bin/python
'''Server side for stage striker'''
import sys
import socket
import signal
import time
import json
from threading import Thread

import redis
from echo_common import MsgType
from echo_common import Status

HOST = '127.0.0.1'
PORT = 8008

REDPASS = 'crampit'
REDIS_CONN = redis.Redis(host='localhost', port=6379, db=0)

_echosocket = None
_clientconn = None

_fighterthreads = []

def signal_handler(sig, frame):
    '''User SigKill handler'''
    print 'You pressed Ctrl+C!'
    _echosocket.close()
    _clientconn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def setup_msg(header, content):
    '''Setup message json'''
    msg = json.dumps({'type': header, 'content': content})
    return msg

class EchoClient(Thread):
    '''Client class created on separate thread per client'''

    def __init__(self, addr):
        Thread.__init__(self)
        self.addr = addr
        print "[+] New server socket thread started for " + addr[0] + ":" + str(addr[1])

    def run(self):
        global _clientconn
        while True:
            data = _clientconn.recv(1024)
            if not data:
                time.sleep(1)
            else:
                try:
                    client_msg = json.loads(data)
                except json.error as msg:
                    print 'Could not load JSON: ' + msg

                if client_msg['type'] == MsgType['USERNAME']:
                    if REDIS_CONN.hexists(client_msg['content'], 'ip'):
                        reply_msg = setup_msg(MsgType['STATUS'], Status['ERROR'])
                        _clientconn.send(reply_msg)
                    else:
                        print client_msg['type']
                        rdata = {"ip":self.addr[0], "port":str(self.addr[1])}
                        REDIS_CONN.hmset(client_msg['content'], rdata)
                        REDIS_CONN.lpush('clients', client_msg['content'])
                        reply_msg = setup_msg(MsgType['STATUS'], Status['OK'])
                        _clientconn.send(reply_msg)
                        # Need to send an okay status here
                        # We're tired and should pause for now take time later to clean up this code
                        # We should use a base with better enumerations and all
                        # E.g. STATUS_OK = 1 but I'm not sure how all of that works in python
                if client_msg['type'] == MsgType['AVAIL']: #likely needs different message type/ if statement or just not in if statement
                    # Setup a thread that polls with this message type every few seconds
                    users = REDIS_CONN.lrange('clients', 0, 10000000)
                    _clientconn.send(json.dumps(users))

                print client_msg

def listen():
    '''Listen for _clientconnections from clients'''

    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res

        global _echosocket, _clientconn

        try:
            _echosocket = socket.socket(af, socktype, proto)
        except socket.error as msg:
            _echosocket = None
            continue
        try:
            _echosocket.bind(sa)
            _echosocket.listen(1)
        except socket.error as msg:
            _echosocket.close()
            _echosocket = None
            continue
        break
    if _echosocket is None:
        print 'could not open socket'
        sys.exit(1)
    _clientconn, addr = _echosocket.accept()
    print 'Connected by', addr
    return addr

def main():
    '''Main function'''

    global _fighterthreads

    while True:
        addr = listen()
        newthread = EchoClient(addr)
        newthread.start()
        _fighterthreads.append(newthread)

    for client_thread in _fighterthreads:
        client_thread.join()

if __name__ == '__main__':
    main()
