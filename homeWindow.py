
from kivy.uix.screenmanager import Screen

class HomeWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.selected_uni = None

    def update_selected_uni(self, uni):
        self.selected_uni = uni
    
    def get_selected_uni(self):
        return self.selected_uni
    