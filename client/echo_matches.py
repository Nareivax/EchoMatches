#!/usr/bin/python
'''Clientside Implementation of Stage Striker including gui'''
import os
import sys
import socket
import signal
import json

from kivy.lang.builder import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from client.lobby import Lobby
from client.select import Select
from echo_common.msg_types import MsgType
from echo_common.status_types import Status

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

def send_msg(content):
    '''Send any message to the server and wait for response'''
    EF_SOCKET = ECHO_SERVER._get_socket()
    EF_SOCKET.sendall(content.encode())
    response = EF_SOCKET.recv(1024)
    print('Received', repr(response))
    return json.loads(response)

def setup_msg(header, content):
    '''Setup message json'''
    msg = json.dumps({'type': header, 'content': content})
    return msg

class Login(Screen):
    '''Class for the login screen on client app'''
    def user_login(self, login_text):
        '''Used to login in a user'''
        app = App.get_running_app()

        login_msg = setup_msg(MsgType['USERNAME'], login_text)
        response = send_msg(login_msg)

        if response['content'] == Status['OK']:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'lobby'

    def reset_login(self):
        '''Clear the text fields'''
        self.ids['login'].text = ""

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

if __name__ == '__main__':

    EF_CLIENT = EchoMatches()
    EF_CLIENT.run()
