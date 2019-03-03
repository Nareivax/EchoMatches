#!/usr/bin/python
'''Clientside Implementation of Stage Striker including gui'''
import os
import sys
import socket
import signal
import json

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from lobby import Lobby
from echo_common import MsgType
from echo_common import Status

###### Host and Port variables for socket connections ######
HOST = '127.0.0.1'
PORT = 8008

EF_SOCKET = None

def signal_handler():
    '''Handles user sigkill'''

    print 'You pressed Ctrl+C!'
    EF_SOCKET.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def connect_server():
    '''Connects to the server'''

    global EF_SOCKET
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            EF_SOCKET = socket.socket(af, socktype, proto)
        except socket.error as msg:
            EF_SOCKET = None
            continue
        try:
            EF_SOCKET.connect(sa)
        except socket.error as msg:
            EF_SOCKET.close()
            EF_SOCKET = None
            continue
        break
    if EF_SOCKET is None:
        print 'Could not connect with EchoFighters Server'
        sys.exit(1)

def send_msg(content):
    '''Send any message to the server and wait for response'''
    EF_SOCKET.sendall(content)
    data = EF_SOCKET.recv(1024)
    print('Received', repr(data))

def setup_msg(header, content):
    '''Setup message json'''
    msg = json.dumps({'type': header, 'content': content})
    return msg

class Login(Screen):
    '''Class for the login screen on client app'''
    def user_login(self, login_text):
        '''Used to login in a user'''
        app = App.get_running_app()

        content = setup_msg(MsgType['USERNAME'], login_text)

        send_msg(content)

        #app.username = login_text
        if login_text == 'quagga':
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'lobby'

            app.config.read(app.app_config())
            app.config.write()

    def reset_login(self):
        '''Clear the text fields'''
        self.ids['login'].text = ""

class EchoMatches(App):
    '''Class for client app'''
    username = StringProperty(None)

    print EF_SOCKET
    print '\n'
    connect_server()
    print EF_SOCKET
    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Lobby(name='lobby'))

        return manager

    def app_config(self):
        '''Configure the app'''
        if not self.username:
            return super(EchoMatches, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if not os.path.exists(conf_directory):
            os.makedirs(conf_directory)

        return super(EchoMatches, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    EchoMatches().run()
