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







class Gerenciador(ScreenManager):
	pass

class Login(Screen):
	pass

class Registro(Screen):
	pass

# para poder usar MDKivy preciso construir com MDApp
class AnalizyApp(MDApp):
	def build(self):
		return Gerenciador()

AnalizyApp().run()