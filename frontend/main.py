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

Window.softinput_mode = 'pan'


# kivymd imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.swiper.swiper import MDSwiperItem
from kivymd.uix.card.card import MDCard


import json
from PIL import Image
from connection import Usuario, Noticias
from scanner import JogosStats




class Gerenciador(MDScreenManager):
    dados_user = {}
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





## fim auxiliares




class Login(MDScreen):
    path = ""
    dialog = None
    texto_alert = ""

    def alert_error_connection(self, *args):
        snackbar = AlertErrorSnackbar(
                text=self.texto_alert,
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
        resposta = user.do_login(email, senha)
        if type(resposta) is dict:
            self.ids.load_spinner.active = True
            path = App.get_running_app().user_data_dir+"/"
            

            store = JsonStore(self.path+"data.json")
            store.put('admiro', permission=resposta['dados']['admin'])

            self.pass_of_login()
        else:
            # melhor usar atributo da funcao do que dessa forma abaixo
            # self.alert_error_connection(texto="Usuario ou Senha Errados!")
            self.texto_alert = resposta
            Clock.schedule_once(self.alert_error_connection, 4)
            # self.alert_error_connection()



    def pass_of_login(self, *args):
        self.load_if = True
        self.path = App.get_running_app().user_data_dir+"/"
        

        store = JsonStore(self.path+'data.json')
        store.put('login_auth', access=True)
        

        App.get_running_app().root.current = "inicio_name"

    def pass_to_register(self, *args):
        App.get_running_app().root.current = "registro_name"



    def timeout_spinner(self, *args):
        self.ids.load_spinner.active = False
      
    def on_press_spinner(self, *args):
        self.ids.load_spinner.active = True
        self.ids.load_spinner.determinate = False
        self.ids.load_spinner.determinate_time = 2
        # depois de 3 segundos executará timeout_spinner
        # desligando o spinner
        Clock.schedule_once(self.timeout_spinner, 3)


    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)

    # tem unbind, se não esse dialog funciona para todas
    # as telas do aplicativo
    def on_pre_leave(self):
        Window.unbind(on_request_close=self.confirmacao)            

    def confirmacao(self, *args, **kwargs):
        # self.add_widget(self.dialog)

    
        self.dialog = MDDialog(
            text="Deseja realmente sair?",
            md_bg_color=(1,1,1,1),
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.closeDialog
                ),

                MDFlatButton(
                    text="Sair",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=App.get_running_app().stop
                ),
            ],
        )
    
        self.dialog.open()

        # tem que retorna um True para on_request_close
        # se não não abre o dialog
        return True

    def closeDialog(self, inst):
        self.dialog.dismiss()


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
            self.alert_error_connection(text="Email já foi cadastrado ou falta de informações")


    def pass_of_register(self, *args):
        App.get_running_app().root.current = "login_name"



## inicio

class Inicio(MDScreen):

    def __init__(self, **kwargs):
        super(Inicio, self).__init__(kwargs)
        self.carregar_jogos()
        self.carregar_noticias()
        self.ids.bottominicio.switch_tab("screen 1")

    def carregar_jogos(self):
        scan = JogosStats()

        jogos = scan.get()

        times = []
        equipes = []
        pontos = []
        jogos_jogados = []
        vitorias = []
        empate = []
        derrotas = []
        saldo_gols = []


        contador = 0
        for it in jogos["Equipe"]:
            times.append(it)
            contador += 1

        for it in jogos["Pontos"]:
            pontos.append(it)

        for it in jogos["J"]:
            jogos_jogados.append(it)

        for it in jogos["V"]:
            vitorias.append(it)

        for it in jogos["E"]:
            empate.append(it)

        for it in jogos["D"]:
            derrotas.append(it)

        for it in jogos["SG"]:
            saldo_gols.append(it)
            

        
        for i in range(contador): 
            
            self.ids.id_jogo_stats.add_widget(
                    Table(
                        text=str(times[i])+" | "+str(pontos[i])+" | "+str(jogos_jogados[i])+" | "+str(vitorias[i])
                        +" | "+str(empate[i])+" | "+str(derrotas[i])+" | "+str(saldo_gols[i])
                                    
                        )
                    )

    def carregar_noticias(self):
        news = Noticias().get()
        print(type(news))
        if type(news) is list:
            for n in news: 
                self.ids.id_noticias.add_widget(
                    MySwiper(text=n["title"], url=n["thumb"], detalhes=n["details"])
                )
        
        

    def on_pre_enter(self):
        self.carregar_jogos()
        self.carregar_noticias()
        self.ids.bottominicio.switch_tab("screen 1")
        Window.bind(on_request_close=self.confirmacao)

    def pass_to(self, name):
        App.get_running_app().root.current = name 

    def on_pre_leave(self, *args):
        self.ids.id_jogo_stats.clear_widgets()
        self.ids.bottominicio.clear_widgets()
        Window.unbind(on_request_close=self.confirmacao)
        

            

    def confirmacao(self, *args, **kwargs):

        self.dialog = MDDialog(
            text="Deseja realmente sair?",
            md_bg_color=(1,1,1,1),
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.closeDialog
                ),

                MDFlatButton(
                    text="Sair",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=App.get_running_app().stop
                ),
            ],
        )
    
        self.dialog.open()

        
        return True

    def closeDialog(self, inst):
        self.dialog.dismiss()



class Table(MDBoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.ids.label_table.text = text

class MySwiper(MDSwiperItem):
    def __init__(self, text='futebol', url='none.png', detalhes="detalhes", **kwargs):
        super().__init__(**kwargs)
        self.ids.id_label_noticias.text = text
        self.ids.id_label_imagens.source = url
        self.ids.id_noticias_descricao.text = detalhes
## fim de inicio



class Menu(MDScreen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(kwargs)
        path = ''
        self.is_admin()


    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)

        # self.path = App.get_running_app().user_data_dir+"/"
        # store = JsonStore(self.path+"data.json")
        # if store.exists('admiro'):
        #     if store.get('admiro')['permission'] == True:
        #         self.ids.content.remove_widget(self.ids.cardAdmin)
        # de alguma forma self.ids não grava o id da classe CardItemMenu Admin
        # minha teoria é que o id é gravado depois de ser adicionados a var self.ids


    def voltar_android(self, *args, **kwargs):
        App.get_running_app().root.current = "inicio_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            App.get_running_app().root.current = "inicio_name"
            return True

        return False


    def is_admin(self):
        self.path = App.get_running_app().user_data_dir+"/"

        store = JsonStore(self.path+"data.json")
        if store.exists('admiro'):
            if store.get('admiro')['permission'] == True:
                self.ids.content.add_widget(CardItemMenuAdmin())

    def do_logout(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')
        if store.exists('login_auth'):
            store.put('login_auth', access=False)

        App.get_running_app().root.current = "login_name"





class CardItemMenuAdmin(MDCard):
    pass



    
# para poder usar MDKivy preciso construir com MDApp
class AnalizyApp(MDApp):
    def build(self):
        return Gerenciador()

AnalizyApp().run()








