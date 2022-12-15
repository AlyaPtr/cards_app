import hashlib
import sqlite3
import connected #Страница для вошедших пользователей
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen


class ConnectedScreen(Screen):
    def disconnect(self):
        self.manager.current = 'login_screen'
