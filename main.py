from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from homeWindow import HomeWindow
from universityWindow import UniversityWindow
from degreeWindow import DegreeWindow
from searchWIndow import SearchWindow
import mysql.connector

class MainApp(MDApp):
    
    comparation_degrees = []

    uni_ID = None
    uni_name = None
    grau_ID = None
    grau_name = None

    last_search = 'bio'

    last_screen = None

    def build(self):
        Window.size = (460, 800)
        # self.theme_cpip install mysql-connector-pythonls.primary_palette = 'Red'
        self.theme_cls.material_style = "M3"
        #kv = Builder.load_file('main.kv')

        #return kv#HomeWindow()

    def change_window(self, window_name, instance = None):
        screen_manager = self.root
        screen_manager.current = window_name
        #screen_manager.transition = NoTransition()

    def connect_bbdd(self):
        conn = mysql.connector.connect(
            host = 'uniplace.cygcilfrqysi.eu-west-3.rds.amazonaws.com',
            user = 'admin',
            passwd = 'Uniplace2023'
        )

        return conn

if __name__ == '__main__':  
    MainApp().run()