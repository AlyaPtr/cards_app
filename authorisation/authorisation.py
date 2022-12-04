from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
import sqlite3
import hashlib
from kivymd.theming import ThemeManager
from kivymd.uix.label import label
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.behaviors import TouchRippleBehavior
from kivy.uix.button import Button
from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton

from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

try:
    conn = sqlite3.connect('../db/database.db')
    cur = conn.cursor()

    # class to call the popup function
    def btn():
        pop_fun()

    # class to build GUI for a popup window
    class P(FloatLayout):
        pass

    # function that displays the content
    def pop_fun():
        show = P()
        window = Popup(title="popup", content=show, size_hint=(None, None), size=(300, 300))
        window.open()

    # class to accept user info and validate it
    class LoginWindow(Screen):
        email = ObjectProperty(None)
        pwd = ObjectProperty(None)

        def validate(self):

            statement = f"SELECT login from authorisation WHERE login='{self.email.text}' AND password = '{hashlib.sha224(self.pwd.text.encode()).hexdigest()}';"
            cur.execute(statement)

            # validating if the email already exists
            if not cur.fetchone():  # An empty result evaluates to False.
                pop_fun()
            else:
                # switching the current screen to display validation result
                sm.current = 'logdata'

                # reset TextInput widget
                self.email.text = ""
                self.pwd.text = ""

    # class to accept sign up info
    class SignupWindow(Screen):
        email = ObjectProperty(None)
        pwd = ObjectProperty(None)

        def signup_btn(self):
            statement = f"SELECT login from authorisation WHERE login='{self.email.text}';"
            cur.execute(statement)

            if self.email.text != "":
                if not cur.fetchone():
                    statement = f"INSERT INTO authorisation(login, password) VALUES('{self.email.text}', '{hashlib.sha224(self.pwd.text.encode()).hexdigest()}');"
                    cur.execute(statement)
                    conn.commit()
            else:
                # if values are empty or invalid show pop up
                pop_fun()

    # class to display validation result
    class LogDataWindow(Screen):
        pass

    # class for managing screens
    class WindowManager(ScreenManager):
        pass


    # kv file
    kv = Builder.load_file('auth.kv')
    sm = WindowManager()

    # reading all the data stored
    # users = pd.read_csv('login.csv')

    # adding screens
    sm.add_widget(LoginWindow(name='login'))
    sm.add_widget(SignupWindow(name='signup'))
    sm.add_widget(LogDataWindow(name='logdata'))

    # class that builds gui
    class AuthMain(App):
        def build(self):
            return sm


    if __name__ == "__main__":
        AuthMain().run()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite: ", error)
finally:
    if conn:
        conn.commit()
        conn.close()
        print("Соединение с SQLite закрыто")
