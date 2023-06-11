
from kivymd.app import MDApp
from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.screenmanager import NoTransition
from kivy.graphics import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.clock import Clock
import webbrowser
import aiosql


class OpenDropButton(GridLayout,Button,ButtonBehavior):
    number = 0 
    status = -1
    sub_ambits = []
    
    def __init__(self,number,sub_ambits, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.sub_ambits = sub_ambits
    
    def on_press(self):
        self.status *= -1
        if self.status > 0: 
            anim = Animation(rot_angle = 0, duration=0.1)
            anim.start(self.ids.arrow)
        else:
            anim = Animation(rot_angle = 90, duration=0.1)
            anim.start(self.ids.arrow)


class DropdownButton(Button):
    
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        Clock.schedule_once(self.get_actual_size_pos, 0)

    def get_actual_size_pos(self,*args):
        return self.size, self.pos

class UniversityWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.ambits = {}
        self.selected_ambit = None
        self.app = MDApp.get_running_app()
        self.conn = self.app.connect_bbdd()
        self.queries = aiosql.from_path('sql/queries.sql', 'pymysql')
        self.uni_ID = None
        self.uni_name = None
        self.selected_grau_ID = None
        self.color = '#C8102E'
   
    def on_pre_enter(self, *args):
        self.ids.ambits_layout.clear_widgets()
        #self.ids.bottom_navigation.switch_tab('info')
        self.ids.bottom_navigation.ids.tab_manager.transition = NoTransition()
        self.ambits_buttons = []
        self.sub_ambits_buttons = []
        home_screen = self.manager.get_screen("home")
        self.uni_ID = home_screen.get_selected_uni()
        self.ids.compare_icon.badge_icon = 'numeric-' + str(len(self.app.comparation_degrees))

        if self.uni_ID == 1:
            self.uni_name = 'UPF'
        elif self.uni_ID == 2:
            self.uni_name = 'UPC'

        self.add_logo()
        self.get_info()
        self.add_ambits() 
        self.update_color()

    
    def update_color(self):
        self.ids.app_name.specific_text_color = self.color
        self.ids.label1.color = self.color
        self.ids.label2.text_color = self.color
        self.ids.label3.icon_left_color_focus = self.color
        self.ids.link.color = self.color

    def update_selected_grau(self, instance):
        self.selected_grau_ID = instance.id
    
    def get_selected_grau(self):
        return self.selected_grau_ID 
        
    def get_info(self):
        try:
            graus = list(self.queries.get_num_graus(self.conn, uni_ID = self.uni_ID))[0][0]
            self.ids.graus.text = str(graus)

            masters = list(self.queries.get_masters(self.conn, uni_ID = self.uni_ID))[0][0]
            self.ids.masters.text = str(masters)

            estudiants = list(self.queries.get_estudiants(self.conn, uni_ID = self.uni_ID))[0][0]
            self.ids.estudiants.text = str(estudiants)

            rector = list(self.queries.get_rector(self.conn, uni_ID = self.uni_ID))[0][0]
            self.ids.rector.text = rector
        except IndexError as e:
            print(e)

        self.ids.nota_2019.text = '11.129'
        self.ids.nota_2020.text = '10.432'
        self.ids.nota_2021.text = '9.789'

    def get_link(self):
        web_uni = list(self.queries.get_web_uni(self.conn, uni_ID = self.uni_ID))[0][0]
        
        return web_uni

    def update_selected_ambit(self, ambit):
        self.selected_ambit = ambit

    def add_ambits(self):
        ambits = self.queries.get_ambits(self.conn, uni_ID = self.uni_ID)
        for ambit_id, ambit in enumerate(ambits):
            btn = OpenDropButton(text = ambit[0], number = ambit_id, sub_ambits=[])
            btn.bind(size=(btn.setter('text_size')))  
            btn.bind(on_press = partial(self.dropdown,btn))
            btn.font_size = 40
            self.ids.ambits_layout.add_widget(btn)
            self.ambits[ambit[0]] = btn
            self.ambits_buttons.append(btn)

    def dropdown(self,chosen_ambit, instance):
        self.update_selected_ambit(instance.text)
        self.ids.ambits_layout.children.index(chosen_ambit)
        graus = self.queries.get_graus(self.conn, uni_ID = self.uni_ID, ambit_name = chosen_ambit.text)
        if chosen_ambit.status < 0: 
            self.show_sub_ambits_buttons(graus,chosen_ambit)
        else:
            for sub_ambit_button in chosen_ambit.sub_ambits:
                    self.ids.ambits_layout.remove_widget(sub_ambit_button)
                    chosen_ambit.sub_ambits = []
        
    def show_sub_ambits_buttons(self,graus,chosen_ambit):
        for ambit_button in self.ambits_buttons:
            if ambit_button.number > chosen_ambit.number:
                self.ids.ambits_layout.remove_widget(ambit_button)
                for sub_ambit_button in ambit_button.sub_ambits:
                    self.ids.ambits_layout.remove_widget(sub_ambit_button)
        for grau in graus:
            btn= DropdownButton(text= grau[1],
                        id= grau[0], 
                        background_normal='',
                        background_color = (1,1,1,1), 
                        color= (0, 0, 0, 1), 
                        size_hint = (1, None), 
                        height=50, 
                        halign = 'left', 
                        valign = 'center', 
                        padding=(20,5),
                        on_release = partial(self.app.change_window, 'degree')) #TODO: mirar si hi ha alguna forma de que no envii la propia instancia
            btn.bind(on_release= self.update_selected_grau) #TODO: com aconseguir el id del grau
            btn.bind(size=btn.setter('text_size'))  
            chosen_ambit.sub_ambits.append(btn) 
            self.sub_ambits_buttons.append(btn)
            self.ids.ambits_layout.add_widget(btn)

        
        for ambit_button in self.ambits_buttons:
            if ambit_button.number > chosen_ambit.number:
                self.ids.ambits_layout.add_widget(ambit_button)
                for sub_ambit_button in ambit_button.sub_ambits:
                        self.ids.ambits_layout.add_widget(sub_ambit_button)
                    
    def add_logo(self):
        self.ids.uni_logo.source = f'assets/{self.uni_name}_logo.png'

    def hyperlink(self, link): 
        webbrowser.open(link)

