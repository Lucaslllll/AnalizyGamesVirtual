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
	# def on_pre_enter(self):
	# 	with open(self.path+"data.json", 'r') as data:
	pass			

class Login(MDScreen):
	
	def do_login(self, *args):
		email = self.ids.id_text_login.text
		senha = self.ids.id_text_password.text


		user = Usuario()
		if user.do_login(email, senha):
			self.pass_of_login()
		else:
			print("errado!!!!")




	def pass_of_login(self, *args):
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
		else:
			print("errado!!!!!")


	def pass_of_register(self, *args):
		App.get_running_app().root.current = "login_name"





# para poder usar MDKivy preciso construir com MDApp
class AnalizyApp(MDApp):
	def build(self):
		return Gerenciador()

AnalizyApp().run()








# dados_carregados = ""
# try:
# 	with open("data.json", "r") as data:
# 		dados_carregados = json.load(data)
# except FileNotFoundError:
# 	pass

# print(dados_carregados)

# for data in dados_carregados:
# 	if data[0] == login and data[1] == senha:
# 		print("logado com sucesso!")
# 		self.on_release()
# 	else:
# 		print("errado seu intruso!")