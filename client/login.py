#!/usr/bin/python
'''Login Page with username and invite code'''

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from echo_common.msg_types import MsgType
from echo_common.status_types import Status

class Login(Screen):
    '''Class for the login screen on client app'''
    def user_login(self, login_text):
        '''Used to login in a user'''
        app = App.get_running_app()

        login_msg = app.setup_msg(MsgType['USERNAME'], login_text)
        response = app.send_msg(login_msg)

        if response['content'] == Status['OK']:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'lobby'

    def reset_login(self):
        '''Clear the text fields'''
        self.ids['login'].text = ""
