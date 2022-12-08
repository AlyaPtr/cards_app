import hashlib
import sqlite3
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

try:
    conn = sqlite3.connect('../db/database.db')
    cur = conn.cursor()


    class LoginScreen(MDScreen):
        def signup_on_press(self):
            self.root.current = 'signup page'

        def clear(self):
            print("clear")
            self.root.ids.user.text = ""
            self.root.ids.password.text = ""

        def logger(self):

            print("logger")

            self.root.ids.welcome_label.text = "Вход"
            self.root.current = 'login page'

            email = self.root.ids.user.text
            pwd = self.root.ids.password.text

            print(email)
            print(pwd)

            statement = f"SELECT login from authorisation WHERE login='{email}' AND password = '{hashlib.sha224(pwd.encode()).hexdigest()}';"
            cur.execute(statement)
            if not cur.fetchone():
                self.root.ids.welcome_label.text = f'Вы ввели неверный логин или пароль'
            else:
                self.root.ids.welcome_label.text = f'Sup {email}!'
            self.clear()

    class SignUpScreen(MDScreen):
        def login_on_press(self):
            self.root.current = 'login page'

        def clear(self):
            print("clear")
            self.root.ids.user.text = ""
            self.root.ids.password.text = ""
        def sign_up(self):
            self.root.ids.welcome_label.text = "Регистрация"
            self.root.current = 'signup page'

            email = self.root.ids.user.text
            pwd = self.root.ids.password.text

            print(email)
            print(pwd)

            statement = f"SELECT login from authorisation WHERE login='{email}';"
            cur.execute(statement)

            if email != "":
                if not cur.fetchone():
                    statement = f"INSERT INTO authorisation(login, password) VALUES('{email}', '{hashlib.sha224(pwd.encode()).hexdigest()}');"
                    cur.execute(statement)
                    conn.commit()
            else:
                self.root.ids.welcome_label.text = f'Пользователь с такой электронной почтой уже существует'
                self.root.ids.user.text = ""
                self.root.ids.password.text = ""

    class MainApp(MDApp):
        def build(self):
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"
            Builder.load_file('auth.kv')
            sm = ScreenManager()
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(SignUpScreen(name='signup'))

            return sm


    MainApp().run()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite: ", error)
finally:
    if conn:
        conn.commit()
        conn.close()
        print("Соединение с SQLite закрыто")
