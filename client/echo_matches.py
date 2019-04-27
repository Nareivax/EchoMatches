#!/usr/bin/python
'''Clientside Implementation of Stage Striker including gui'''

import sys
import signal
import json

from kivy.lang.builder import Builder
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager

from client.lobby import Lobby
from client.login import Login
from client.select import Select

###### Host and Port variables for socket connections ######
HOST = '127.0.0.1'
PORT = 8008

ECHO_SERVER = None
EF_CLIENT = None

def signal_handler():
    '''Handles user sigkill'''

    EF_SOCKET = Select._get_socket()
    print('You pressed Ctrl+C!')
    EF_SOCKET.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class EchoMatches(App):
    '''Class for client app'''

    def build(self):
        Builder.load_file('select.kv')
        manager = ScreenManager()

        global ECHO_SERVER
        ECHO_SERVER = Select(name='select')

        manager.add_widget(ECHO_SERVER)
        manager.add_widget(Login(name='login'))
        manager.add_widget(Lobby(name='lobby'))

        return manager

    def send_msg(self, content):
        '''Send any message to the server and wait for response'''
        EF_SOCKET = ECHO_SERVER._get_socket()
        EF_SOCKET.sendall(content.encode())
        response = EF_SOCKET.recv(1024)
        print('Received', repr(response))
        return json.loads(response)

    def setup_msg(self, header, content):
        '''Setup message json'''
        msg = json.dumps({'type': header, 'content': content})
        return msg

if __name__ == '__main__':

    EF_CLIENT = EchoMatches()
    EF_CLIENT.run()
