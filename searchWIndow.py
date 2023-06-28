from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
import aiosql
import yaml
import random

class SearchWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.conn = self.app.connect_bbdd()
        self.queries = aiosql.from_path('sql/queries.sql', 'pymysql')
        with open("tablas_tipo.yaml", 'r') as stream:
            self.tablas_tipo = yaml.safe_load(stream)
    
    def on_leave(self, *args):
        self.app.last_screen = 'search'


    def on_pre_enter(self, *args):
        view_area = self.ids.search_area
        view_area.clear_widgets()

        nota = random.uniform(6, 12)

        home_screen = self.manager.get_screen('home')
        grau_name = home_screen.ids.search_field.text

        self.ids.search_field.text = grau_name
        results = list(self.queries.search_graus(self.conn, grau_name = '%' + grau_name + '%'))
        print(results)
        for result in results:
            varianza = random.uniform(-1, 1)
            uni_name = self.tablas_tipo['unis'][result[1]]['name']
            logo = self.tablas_tipo['unis'][result[1]]['logo_path']
            item = SearchItemCard(logo=logo, grau_name= result[0], grau_ID=result[2], uni_name=uni_name, uni_ID=result[1], nota= str(round(nota + varianza, 3)), loc= self.tablas_tipo['unis'][result[1]]['loc'])
            view_area.add_widget(item)

    def search_grau(self):
        view_area = self.ids.search_area
        view_area.clear_widgets()

        nota = random.uniform(6, 12)

        grau_name = self.ids.search_field.text
        home_screen = self.manager.get_screen('home')
        home_screen.ids.search_field.text = grau_name

        results = list(self.queries.search_graus(self.conn, grau_name = '%' + grau_name + '%'))
        print(results)
        for result in results:
            varianza = random.uniform(-1, 1)
            uni_name = self.tablas_tipo['unis'][result[1]]['name']
            logo = self.tablas_tipo['unis'][result[1]]['logo_path']
            item = SearchItemCard(logo=logo, grau_name= result[0], grau_ID= result[2], uni_name=uni_name, uni_ID=result[1], nota= str(round(nota + varianza, 3)), loc= self.tablas_tipo['unis'][result[1]]['loc'])

            view_area.add_widget(item)
        

    def on_click(self, instance):
        self.app.uni_name = instance.uni_name
        self.app.uni_ID = instance.uni_ID
        self.app.grau_name = instance.grau_name
        self.app.grau_ID = instance.grau_ID
        self.app.change_window('degree')

    def go_back(self):
        home_screen = self.manager.get_screen('home')
        home_screen.ids.search_field.text = ''
        self.app.change_window('home')


class SearchItemCard(MDCard):
    logo = StringProperty()
    grau_name = StringProperty()
    grau_ID = NumericProperty()
    uni_name = StringProperty()
    uni_ID = NumericProperty()
    nota = StringProperty()
    loc = StringProperty()