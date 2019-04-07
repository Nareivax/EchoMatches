#!/usr/bin/python
'''Login Page with username and invite code'''

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from echo_common.msg_types import MsgType
from echo_common.status_types import Status

class Login(Screen):
    '''Class for the login screen on client app'''
    def user_login(self, login_text, login_type):
        '''Used to login in a user'''
        app = App.get_running_app()

        login_msg = app.setup_msg(login_type, login_text)
        response = app.send_msg(login_msg)
        return response

    def join_lobby(self, login_text):
        '''Join an already created lobby'''
        response = self.user_login(login_text, MsgType['JOIN'])

        if response['content'] == Status['OK']:
            invite_popup = InviteDialog(self)
            invite_popup.open()
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'lobby'

    def create_lobby(self, login_text):
        '''Start a new lobby'''
        response = self.user_login(login_text, MsgType['CREATE'])

        if response['content'] == Status['OK']:
            self.manager.current = 'lobby'

    def reset_login(self):
        '''Clear the text fields'''
        self.ids['login'].text = ""

class InviteDialog(Popup):

    def __init__(self, parent, *args):
        super(InviteDialog, self).__init__(*args)

    def on_error(self, inst, text):
        if text:
            self.lb_error.size_hint_y = 1
            self.size = (400, 150)
        else:
            self.lb_error.size_hint_y = None
            self.lb_error.height = 0
            self.size = (400, 120)

    def check_invite(self):
        print('hi')

    def _cancel(self):
        self.dismiss()
