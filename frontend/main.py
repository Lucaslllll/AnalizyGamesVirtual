# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

# kivymd imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
import json



from connection import Usuario
from scanner import JogosStats


class Gerenciador(MDScreenManager):
    dados_user = []
    userON = True
    path = ""
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.path = App.get_running_app().user_data_dir+"/"

    #     try:
    #         with open("data.json", 'r') as data:
    #             self.dados_user = json.load(data)
    #     except FileNotFoundError:
    #         self.userON = False

    #     userON = self.dados_user['userON']
    #     print(userON)

    #     if userON == True:
    #         self.current = "inicio_name"





class Login(MDScreen):
    path = ""

    def do_login(self, *args):
        email = self.ids.id_text_login.text
        senha = self.ids.id_text_password.text


        user = Usuario()
        if user.do_login(email, senha):
            self.ids.load_spinner.active = True
            self.pass_of_login()
        elif user.do_login(email, senha) == None:
            print("Conexão não estabelecida com o servidor!")
        else:
            print("errado!!!!")




    def pass_of_login(self, *args):
        self.load_if = True
        self.path = App.get_running_app().user_data_dir+"/"
        
        print(self.ids.load_spinner.active)
        with open("data.json", "w") as data:
            json.dump({"userON":True}, data)
        

        App.get_running_app().root.current = "inicio_name"

    def pass_to_register(self, *args):
        App.get_running_app().root.current = "registro_name"


class Registro(MDScreen):
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
            print("Conexão não estabelecida com o servidor!")
        else:
            print("errado!!!!!")


    def pass_of_register(self, *args):
        App.get_running_app().root.current = "login_name"




class Inicio(MDScreen):


    def carregar_jogos(self):
        scan = JogosStats()

        jogos = scan.get()

        # self.ids.box.add_widget(Tarefa(text=tarefa))
        print("AAAAAAA")
        for jogo in jogos:
            print(jogo["full_time_result"])
            self.ids.id_jogo_stats.add_widget(Table(text=str(jogo["time"]+" | "+jogo["home_team"]+" X "+jogo["away_team"]+" = ")
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








# dados_carregados = ""
# try:
#   with open("data.json", "r") as data:
#       dados_carregados = json.load(data)
# except FileNotFoundError:
#   pass

# print(dados_carregados)

# for data in dados_carregados:
#   if data[0] == login and data[1] == senha:
#       print("logado com sucesso!")
#       self.on_release()
#   else:
#       print("errado seu intruso!")

# jogo["time"]+" | "+jogo["home_team"]+" | "+jogo["away_team"]+" | "+
#                                          jogo["full_time_result"]+" | "+jogo["under_over"]+" | "+jogo["both_teams_to_score"]+
#                                          " | "+jogo["double_chance"]