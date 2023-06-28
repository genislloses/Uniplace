
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

class HomeWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
    
    def on_leave(self, *args):
        self.app.last_screen = 'home'
    
    def update_selected_uni(self, uni):
        self.app.uni_ID = uni
    

    