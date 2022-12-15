import hashlib
import sqlite3
import connected #Страница для вошедших пользователей
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

try:
    conn = sqlite3.connect('../db/database.db')
    cur = conn.cursor()

    class LoginScreen(Screen):
        def logger(self):

            email = self.ids.user.text
            pwd = self.ids.password.text

            print(email)
            print(pwd)

            statement = f"SELECT login from authorisation WHERE login='{email}' AND password = '{hashlib.sha224(pwd.encode()).hexdigest()}';"
            cur.execute(statement)
            if not cur.fetchone():
                self.ids.welcome_label.text = "Вы ввели неверный логин или пароль"
            else:
                self.manager.current = 'connected_screen'
                self.ids.welcome_label.text = f'Sup {email}!'

    class SignUpScreen(Screen):
        pass

    class MainApp(MDApp):
        def __init__(self, **kwargs):
            self.title = "My Material Application"
            super().__init__(**kwargs)

        def sign_up(self):\

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

        def build(self):
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"
            self.root = Builder.load_file("authorization.kv")


    MainApp().run()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite: ", error)
finally:
    if conn:
        conn.commit()
        conn.close()
        print("Соединение с SQLite закрыто")
