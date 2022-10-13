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
from kivymd.uix.dialog import MDDialog
from kivymd.uix.swiper.swiper import MDSwiperItem
from kivymd.uix.card.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield.textfield import MDTextField

import json
from PIL import Image
from connection import Usuario, Noticias
from scanner import JogosStats


Window.softinput_mode = 'pan'
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')




class Gerenciador(MDScreenManager):
    path = ""
    admin_is = False
    noticia_atual = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = App.get_running_app().user_data_dir+"/"
        
            
        store = JsonStore(self.path+"data.json")
        if store.exists('login_auth'):
            if store.get('login_auth')['access'] == True:
                self.current = "admin_name"




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

            self.path = App.get_running_app().user_data_dir+"/"
            store = JsonStore(self.path+'data.json')
            store.put('user', id=resposta['dados']['id'])    
            
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

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)


    def voltar_android(self, *args, **kwargs):
        App.get_running_app().root.current = "login_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            App.get_running_app().root.current = "login_name"
            return True

        return False


## inicio

class Inicio(MDScreen):

        
    def carregar_jogos(self):
        scan = JogosStats()

        jogos = scan.get()

        if len(jogos) != 0:

            times = ['Equipe']
            pontos = ['Pontos']
            jogos_jogados = ['J']
            vitorias = ['V']
            empate = ['E']
            derrotas = ['D']
            saldo_gols = ['SG']


            contador = len(jogos["Equipe"])

            for it in jogos["Equipe"]:
                times.append(it)

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
                

            for i in range(0, contador+1): 
                self.ids.id_jogo_stats.add_widget(
                        Table(
                            text=str(times[i])+" | "+str(pontos[i])+" | "+str(jogos_jogados[i])+" | "+str(vitorias[i])
                            +" | "+str(empate[i])+" | "+str(derrotas[i])+" | "+str(saldo_gols[i])
                                        
                            )
                        )

    def carregar_noticias(self):
        news = Noticias().get()
        if type(news) is list:
            for n in news: 
                self.ids.id_noticias.add_widget(
                    MySwiper(text=n["title"], url=n["thumb"], detalhes=n["preview"], id_noticia=n['id'])
                )
    
    def ir_noticia(self, id_noticia):
        App.get_running_app().root.noticia_atual = id_noticia
        App.get_running_app().root.current = "noticia_name"

     

    def on_pre_enter(self):
        self.carregar_jogos()
        self.carregar_noticias()
        self.ids.bottominicio.switch_tab("screen 1")
        Window.bind(on_request_close=self.confirmacao)
        # self.ids.update({child.id:child for child in self.children})
        # print(self.ids.id_noticias.children)

    def pass_to(self, name):
        store = JsonStore(App.get_running_app().user_data_dir+"/data.json")
        if store.exists('user'):
            user = Usuario().buscar_dados(pk=store.get('user')['id'])
        
            if type(user) is dict: 
                App.get_running_app().root.admin_is = user['admin']


        App.get_running_app().root.current = name 
        


    def on_pre_leave(self, *args):
        self.ids.id_jogo_stats.clear_widgets()
        for child in self.ids.id_noticias.children:
            child.clear_widgets()
        
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
    def __init__(self, text='futebol', url='none.png', detalhes="detalhes", id_noticia=None, **kwargs):
        super().__init__(**kwargs)
        self.ids.id_label_noticias.text = text
        self.ids.id_label_imagens.source = url
        self.ids.id_noticias_descricao.text = detalhes
        if id_noticia != None: 
            self.id_da_noticia = id_noticia


## fim de inicio


class Noticia(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Home",
                "height": 56,
                "on_release": lambda x="Home": self.menu_callback("inicio_name"),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Menu",
                "height": 56,
                "on_release": lambda x="Menu": self.menu_callback("menu_name"),
            }

        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )


    def DropApp(self, instance_action_top_appbar_button):
        self.menu.caller = instance_action_top_appbar_button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        App.get_running_app().root.current = text_item


    def on_pre_enter(self):
        id_da_noticia = App.get_running_app().root.noticia_atual
        news = Noticias().get(id_noticia=id_da_noticia)
        if type(news) is dict:
            self.ids.title_noticia.text = news['title']
            self.ids.details_noticia.text = news['details']

        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)

    def voltar_android(self, *args, **kwargs):
        App.get_running_app().root.current = "inicio_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            App.get_running_app().root.current = "inicio_name"
            return True

        return False



## menu

class CustomDropMenu(MDDropdownMenu):
    pass


class Menu(MDScreen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        path = ''
        


    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        self.is_admin()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)
        if App.get_running_app().root.admin_is == True:
            self.ids.content.remove_widget(self.ids.content.children[0])

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
        if App.get_running_app().root.admin_is == True:
            self.ids.content.add_widget(CardItemMenuAdmin())


    def do_logout(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')
        if store.exists('login_auth'):
            store.put('login_auth', access=False)

        App.get_running_app().root.current = "login_name"



class CardItemMenuAdmin(MDCard):
    pass

# fim do menu


## admin

class Admin(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.button_search = MDTextField(
            # id="id_button_search",
            hint_text="Search",
            line_color_normal= (1, 0, 1, 1),
            text_color_focus= (1, 1, 1, 1),
            on_release=lambda x: self.button_search_callback("name"),

        )
        

    def SearchApp(self, instance_button):
        self.button_search.caller = instance_button
        self.ids.toolbarNoticia.add_widget(self.button_search)
        
    def button_search_callback(self, name):
        # search_text = self.ids.id_button_search.text
        print(name)


# fim do admin


    
# para poder usar MDKivy preciso construir com MDApp inves de App do kivy
class AnalizyApp(MDApp):
    def build(self):
        return Gerenciador()

AnalizyApp().run()








