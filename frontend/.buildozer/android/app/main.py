# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore



# kivymd imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.button import MDFlatButton
import json


from PIL import Image
from connection import Usuario
from scanner import JogosStats


class Gerenciador(MDScreenManager):
    dados_user = {}
    userON = True
    path = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = App.get_running_app().user_data_dir+"/"
        print(self.path)
        store = JsonStore(self.path+"data.json")
        if store.exists('login_auth'):
            if store.get('login_auth')['access'] == True:
                self.current = "inicio_name"




## classes auxiliares


class AlertErrorSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")



##




class Login(MDScreen):
    path = ""

    def alert_error_connection(self, text="Conexão não estabelecida com o servidor!", *args):
        snackbar = AlertErrorSnackbar(
                text=text,
                icon="information",
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[
                    MDFlatButton(text="Fechar", text_color=(1, 1, 1, 1),
                                theme_text_color='Custom')
                ]
            )
        snackbar.size_hint_x = (
            Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width
        snackbar.open()

    def do_login(self, *args):
        email = self.ids.id_text_login.text
        senha = self.ids.id_text_password.text


        user = Usuario()
        if user.do_login(email, senha):
            self.ids.load_spinner.active = True
            self.pass_of_login()
        elif user.do_login(email, senha) == None:
            Clock.schedule_once(self.alert_error_connection, 4)

        else:
            self.alert_error_connection(text="Usuario ou Senha Errados!")


    def timeout_spinner(self, *args):
        self.ids.load_spinner.active = False
      
    def on_press_spinner(self, *args):
        self.ids.load_spinner.active = True
        self.ids.load_spinner.determinate = False
        self.ids.load_spinner.determinate_time = 2
        # depois de 3 segundos executará timeout_spinner
        # desligando o spinner
        Clock.schedule_once(self.timeout_spinner, 3)
        

    def pass_of_login(self, *args):
        self.load_if = True
        self.path = App.get_running_app().user_data_dir+"/"
        

        store = JsonStore(self.path+'data.json')
        store.put('login_auth', access=True)
        

        App.get_running_app().root.current = "inicio_name"



    def pass_to_register(self, *args):
        App.get_running_app().root.current = "registro_name"


class Registro(MDScreen):

    def alert_error_connection(self, text, *args):
        snackbar = AlertErrorSnackbar(
                text=text,
                icon="information",
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[
                    MDFlatButton(text="Fechar", text_color=(1, 1, 1, 1),
                                theme_text_color='Custom')
                ]
            )
        snackbar.size_hint_x = (
            Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width
        snackbar.open()

    def do_register(self, *args):
        data = {
            "first_name" : self.ids.id_first_name.text,
            "last_name" : self.ids.id_last_name.text,
            "email" : self.ids.id_email.text,
            "password" : self.ids.id_password.text
        }

        user = Usuario()
        
        if user.do_register(data):
            self.pass_of_register()
        elif user.do_register(data) == None:
            self.alert_error_connection(text="Conexão não estabelecida com o servidor!")
        else:
            self.alert_error_connection(text="Email já foi cadastrado")


    def pass_of_register(self, *args):
        App.get_running_app().root.current = "login_name"




class Inicio(MDScreen):


    def carregar_jogos(self):
        scan = JogosStats()

        jogos = scan.get()

        # self.ids.box.add_widget(Tarefa(text=tarefa))
        #print("Debug AAAAAAA")
        for jogo in jogos:
            # print(jogo["full_time_result"])
            self.ids.id_jogo_stats.add_widget(
                Table(text=str(jogo["time"]+" | "+jogo["home_team"]+" X "+jogo["away_team"]+" = ")
                                    ))
    def on_pre_enter(self):
        self.carregar_jogos()

    def pass_to(self, name):
        App.get_running_app().root.current = name 

    def on_pre_leave(self, *args):
        self.ids.id_jogo_stats.clear_widgets()

class Table(MDBoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.ids.label_table.text = text


class Placares(MDScreen):
    pass


class Menu(MDScreen):
    pass

    
# para poder usar MDKivy preciso construir com MDApp
class AnalizyApp(MDApp):
    def build(self):
        return Gerenciador()

AnalizyApp().run()








