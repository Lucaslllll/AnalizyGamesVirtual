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
import json



from connection import Usuario


class Gerenciador(ScreenManager):
	pass

class Login(MDScreen):
	
	def do_login(self, *args):
		login = self.ids.id_text_login.text
		senha = self.ids.id_text_password.text

		dados_carregados = ""


		try:
			with open("data.json", "r") as data:
				dados_carregados = json.load(data)
		except FileNotFoundError:
			pass
		
		print(dados_carregados)
		
		for data in dados_carregados:
			if data[0] == login and data[1] == senha:
				print("logado com sucesso!")
				self.on_release()
			else:
				print("errado seu intruso!")
		#print(login + " " + senha)


	def on_release(self, *args):
		App.get_running_app().root.current = "registro_name"




class Registro(MDScreen):
	def on_pre_enter(self):
		users = Usuario()
		data_list = []

		for data in users.buscar_dados():
			self.ids.test_api_id.add_widget(Usuarios(data['first_name']))
			data_list.append(data)
			print(data)


class Usuarios(BoxLayout):
	def __init__(self, first_name, **kwargs):
		super().__init__(**kwargs)
		self.ids.label_id_test.text = first_name


# para poder usar MDKivy preciso construir com MDApp
class AnalizyApp(MDApp):
	def build(self):
		return Gerenciador()

AnalizyApp().run()