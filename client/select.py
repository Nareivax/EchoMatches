#!/usr/bin/python
'''Code for the server connect interaction'''

import sys
import socket

from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Select(Screen):
    '''Class for the server select screen on client app'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.EF_SOCKET = None

    def connect_server(self, server_ip, server_port):
        '''Connects to the server'''

        HOST = server_ip
        PORT = int(server_port)
        app = App.get_running_app()

        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.EF_SOCKET = socket.socket(af, socktype, proto)
            except socket.error as msg:
                self.EF_SOCKET = None
                continue
            try:
                self.EF_SOCKET.connect(sa)
            except socket.error as msg:
                self.EF_SOCKET.close()
                self.EF_SOCKET = None
                continue
            break

        if self.EF_SOCKET is None:
            popup = Popup(title='Connection Error',
                content=Label(text='Could Not Connect to Server: ' + HOST + ':' + str(PORT)),
                size_hint=(None, None), size=(400, 200))
            popup.open()
            print('Could not connect with Server')
            self.reset_inputs()
        else:
            self.manager.transition = SlideTransition(direction="up")
            self.manager.current = 'login'

    def _get_socket(self):
        return self.EF_SOCKET

    def reset_inputs(self):
        '''Clear the text fields'''
        self.ids['server_ip'].text = ""
        self.ids['server_port'].text = ""
