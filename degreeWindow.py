from kivymd.app import MDApp
from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.screenmanager import NoTransition
from kivy.graphics import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.clock import Clock
import webbrowser
import aiosql
import random
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
import yaml

class OpenDropButton(GridLayout, Button, ButtonBehavior):
    number = 0
    status = -1
    subjects = []

    def __init__(self, number, subjects, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.subjects = subjects

    def on_press(self):
        self.status *= -1
        if self.status > 0:
            anim = Animation(rot_angle=0, duration=0.1)
            anim.start(self.ids.arrow)
        else:
            anim = Animation(rot_angle=90, duration=0.1)
            anim.start(self.ids.arrow)


class DropdownButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.get_actual_size_pos, 0)

    def get_actual_size_pos(self, *args):
        return self.size, self.pos


class ContentBox(MDGridLayout):
    pass


class IndicatorsBox(MDBoxLayout):
    rendiment = StringProperty()
    abandonament = StringProperty()
    homes = StringProperty()
    dones = StringProperty()


class DegreeWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.courses = {}
        self.selected_course = None
        self.app = MDApp.get_running_app()
        self.conn = self.app.connect_bbdd()
        self.queries = aiosql.from_path('sql/queries.sql', 'pymysql')
        with open("tablas_tipo.yaml", 'r') as stream:
            self.tablas_tipo = yaml.safe_load(stream)

    def on_leave(self, *args):
        self.app.last_screen = 'degree'


    def on_pre_enter(self, *args):
        print('UNI ID:  ', self.app.uni_ID)
        print('UNI NAME:  ', self.app.uni_name)
        print('GRAU ID:  ', self.app.grau_ID)
        print('GRAU NAME:  ', self.app.grau_name)

        print(self.app.comparation_degrees)

        self.ids.logo.source = self.tablas_tipo['unis'][self.app.uni_ID]['logo_path']

        self.abandonament = round(random.uniform(25, 55), 2)
        self.rendiment = round(random.uniform(60, 90), 2)
        self.homes = round(random.uniform(35, 65), 2)
        self.dones = round(100 - self.homes, 2)

        panel = self.ids.panel
        panel.clear_widgets()
        panels_list = ['Descripció', 'Sortides laborals', 'Ponderacions']

        for i in panels_list:
            md_panel = MDExpansionPanel(content=ContentBox(),
                                        panel_cls=MDExpansionPanelOneLine(text = i))
            md_panel.content.ids.panel_text.text = self.tablas_tipo['graus']['A'][i]
            panel.add_widget(md_panel)

        md_panel = MDExpansionPanel(content=IndicatorsBox(rendiment = str(self.rendiment)+ '%', abandonament = str(self.abandonament)+ '%', homes = str(self.homes)+ '%', dones = str(self.dones)+'%'),
                                    panel_cls=MDExpansionPanelOneLine(text='Indicadors'))
        panel.add_widget(md_panel)
        self.ids.courses_layout.clear_widgets()
        self.ids.bottom_navigation.switch_tab('info')
        self.ids.bottom_navigation.ids.tab_manager.transition = NoTransition()
        self.courses_buttons = []
        self.subjects_buttons = []
        self.add_cursos()
        self.ids.compare_icon.badge_icon = 'numeric-' + str(len(self.app.comparation_degrees))
        self.ids.path.text = f'{self.app.uni_name} > {self.app.grau_name}'
        self.ids.screen_title.text = self.app.grau_name

        self.uni_screen = self.manager.get_screen("uni")

        self.places = random.randint(6, 20) * 5
        self.nota = round(random.uniform(6, 12.500), 3)
        self.ids.places.text = str(self.places)
        self.ids.nota_22.text = str(self.nota)
        self.ids.nota_21.text = str(round(self.nota - 0.146, 3))
        self.ids.nota_20.text = str(round(self.nota - 0.487, 3))

        if self.app.grau_ID == 1:
            self.ids.nota_22.text = '10,352'
            self.ids.nota_21.text = '9,966'
            self.ids.nota_20.text = '9,798'
            self.ids.places.text = '55'
            self.nota = '10,352'
            self.places = 55
        elif self.app.grau_ID  == 77:
            self.ids.nota_22.text = '10,818'
            self.ids.nota_21.text = '10,432'
            self.ids.nota_20.text = '9,998'
            self.ids.places.text = '360'
            self.nota = '10,818'
            self.places = 360
        

        if len(self.app.comparation_degrees) == 2 or self.app.grau_ID in self.app.comparation_degrees:
            self.ids.compare_button.disabled = True
        else:
            self.ids.compare_button.disabled = False

        # accessing Compare Screen 2nd degree name label text"""
        #print(self.ids.compare_box.ids.s_degree_name.text)

    def update_selected_course(self, course):
        self.selected_course = course

    def add_cursos(self):
        courses = ['1r curs', '2n curs', '3r curs', '4t curs'] 
        for course_id, course in enumerate(courses):
            btn = OpenDropButton(text=course, number=course_id, subjects=[])
            btn.bind(size=(btn.setter('text_size')))
            btn.bind(on_press=partial(self.dropdown, btn))
            btn.font_size = 40
            self.ids.courses_layout.add_widget(btn)
            self.courses[course] = btn
            self.courses_buttons.append(btn)

    def dropdown(self, chosen_curs, instance):
        self.update_selected_course(instance.text)
        self.ids.courses_layout.children.index(chosen_curs)
        assignatures = self.queries.get_assignatures(self.conn, grau_ID=self.app.grau_ID, curs=chosen_curs.number + 1)
        assignatures = [i[0] for i in assignatures]

        #CHECK ASSIGNATURES
        if len(assignatures) == 0:
            assignatures = self.queries.get_assignatures(self.conn, grau_ID=random.choice([1, 2, 3, 4, 6]), curs=chosen_curs.number + 1)
            assignatures = [i[0] for i in assignatures]

        if chosen_curs.status < 0:
            self.show_subjects_buttons(assignatures, chosen_curs)
        else:
            for subject_button in chosen_curs.subjects:
                self.ids.courses_layout.remove_widget(subject_button)
                chosen_curs.subjects = []

    def show_subjects_buttons(self, enginyeries, chosen_course):
        for course_button in self.courses_buttons:
            if course_button.number > chosen_course.number:
                self.ids.courses_layout.remove_widget(course_button)
                for subjects_button in course_button.subjects:
                    self.ids.courses_layout.remove_widget(subjects_button)
        for enginyeria in enginyeries:
            btn = DropdownButton(text=enginyeria,
                                 background_normal='',
                                 background_color=(1, 1, 1, 1),
                                 color=(0, 0, 0, 1),
                                 size_hint=(1, None),
                                 height=50,
                                 halign='left',
                                 valign='center',
                                 padding=(20, 5),
                                 on_release=partial(self.app.change_window,
                                                    'degree'))  # TODO: mirar si hi ha alguna forma de que no envii la propia instancia
            btn.bind(size=btn.setter('text_size'))
            chosen_course.subjects.append(btn)
            self.subjects_buttons.append(btn)
            self.ids.courses_layout.add_widget(btn)

        for course_button in self.courses_buttons:
            if course_button.number > chosen_course.number:
                self.ids.courses_layout.add_widget(course_button)
                for subjects_button in course_button.subjects:
                    self.ids.courses_layout.add_widget(subjects_button)

    def add_grau_to_compare(self):
        self.app.comparation_degrees.append(self.app.grau_ID)
        self.ids.compare_icon.badge_icon = 'numeric-' + str(int(self.ids.compare_icon.badge_icon.split('-')[1]) + 1)
        self.ids.compare_button.disabled = True
        if len(self.app.comparation_degrees) == 1:
            grau_name = self.app.grau_name
            uni_name = self.tablas_tipo['unis'][self.app.uni_ID]['siglas']
            loc = self.tablas_tipo['unis'][self.app.uni_ID]['loc']
            credits = '240'
            link = 'LINK'

            #GRAU
            self.ids.compare_box_grau.ids.comp1_grau_name.text = grau_name
            self.ids.compare_box_grau.ids.comp1_uni_name.text = uni_name
            self.ids.compare_box_grau.ids.comp1_nota.text = str(self.nota)
            self.ids.compare_box_grau.ids.comp1_places.text = str(self.places)
            self.ids.compare_box_grau.ids.comp1_loc.text = loc
            self.ids.compare_box_grau.ids.comp1_rendiment.text = str(self.rendiment) + '%'
            self.ids.compare_box_grau.ids.comp1_abandonament.text = str(self.abandonament) + '%'
            self.ids.compare_box_grau.ids.comp1_homes.text = str(self.homes)+ '%'
            self.ids.compare_box_grau.ids.comp1_dones.text = str(self.dones)+ '%'
            self.ids.compare_box_grau.ids.comp1_credits.text = credits
            self.ids.compare_box_grau.ids.comp1_link.text = link
            self.ids.compare_box_grau.ids.comp1_link.bind(on_release= partial(self.hyperlink,'https://www.upf.edu/web/universitat/grau-en-enginyeria-matematica-en-ciencia-de-dades'))
            #UNI
            self.uni_screen.ids.compare_box_uni.ids.comp1_grau_name.text = grau_name
            self.uni_screen.ids.compare_box_uni.ids.comp1_uni_name.text = uni_name
            self.uni_screen.ids.compare_box_uni.ids.comp1_nota.text = str(self.nota)
            self.uni_screen.ids.compare_box_uni.ids.comp1_places.text = str(self.places)
            self.uni_screen.ids.compare_box_uni.ids.comp1_loc.text = loc
            self.uni_screen.ids.compare_box_uni.ids.comp1_rendiment.text = str(self.rendiment) + '%'
            self.uni_screen.ids.compare_box_uni.ids.comp1_abandonament.text = str(self.abandonament) + '%'
            self.uni_screen.ids.compare_box_uni.ids.comp1_homes.text = str(self.homes)+ '%'
            self.uni_screen.ids.compare_box_uni.ids.comp1_dones.text = str(self.dones)+ '%'
            self.uni_screen.ids.compare_box_uni.ids.comp1_credits.text = credits
            self.uni_screen.ids.compare_box_uni.ids.comp1_link.text = link
            self.uni_screen.ids.compare_box_uni.ids.comp1_link.bind(on_release= partial(self.hyperlink,'https://www.upf.edu/web/universitat/grau-en-enginyeria-matematica-en-ciencia-de-dades'))

        else:
            grau_name = self.app.grau_name
            uni_name = self.tablas_tipo['unis'][self.app.uni_ID]['siglas']
            loc = self.tablas_tipo['unis'][self.app.uni_ID]['loc']
            credits = '240'
            link = 'LINK'

            #GRAU
            self.ids.compare_box_grau.ids.comp2_grau_name.text = grau_name
            self.ids.compare_box_grau.ids.comp2_uni_name.text = uni_name
            self.ids.compare_box_grau.ids.comp2_nota.text = str(self.nota)
            self.ids.compare_box_grau.ids.comp2_places.text = str(self.places)
            self.ids.compare_box_grau.ids.comp2_loc.text = loc
            self.ids.compare_box_grau.ids.comp2_rendiment.text = str(self.rendiment) + '%'
            self.ids.compare_box_grau.ids.comp2_abandonament.text = str(self.abandonament) + '%'
            self.ids.compare_box_grau.ids.comp2_homes.text = str(self.homes)+ '%'
            self.ids.compare_box_grau.ids.comp2_dones.text = str(self.dones)+ '%'
            self.ids.compare_box_grau.ids.comp2_credits.text = credits
            self.ids.compare_box_grau.ids.comp2_link.text = link
            self.ids.compare_box_grau.ids.comp2_link.bind(on_release= partial(self.hyperlink,'https://www.ub.edu/indicadorsVSMA/ensenyament.php?codi=G1051'))

            #UNI
            self.uni_screen.ids.compare_box_uni.ids.comp2_grau_name.text = grau_name
            self.uni_screen.ids.compare_box_uni.ids.comp2_uni_name.text = uni_name
            self.uni_screen.ids.compare_box_uni.ids.comp2_nota.text = str(self.nota)
            self.uni_screen.ids.compare_box_uni.ids.comp2_places.text = str(self.places)
            self.uni_screen.ids.compare_box_uni.ids.comp2_loc.text = loc
            self.uni_screen.ids.compare_box_uni.ids.comp2_rendiment.text = str(self.rendiment) + '%'
            self.uni_screen.ids.compare_box_uni.ids.comp2_abandonament.text = str(self.abandonament) + '%'
            self.uni_screen.ids.compare_box_uni.ids.comp2_homes.text = str(self.homes)+ '%'
            self.uni_screen.ids.compare_box_uni.ids.comp2_dones.text = str(self.dones)+ '%'
            self.uni_screen.ids.compare_box_uni.ids.comp2_credits.text = credits
            self.uni_screen.ids.compare_box_uni.ids.comp2_link.text = link
            self.uni_screen.ids.compare_box_uni.ids.comp2_link.bind(on_release= partial(self.hyperlink,'https://www.ub.edu/indicadorsVSMA/ensenyament.php?codi=G1051'))
      
            
    def delete_comparation(self):
        self.app.comparation_degrees = []
        self.ids.compare_button.disabled = False
        self.ids.compare_icon.badge_icon = 'numeric-0'
        self.uni_screen.ids.compare_icon.badge_icon = 'numeric-0'
        
        #GRAU
        self.ids.compare_box_grau.ids.comp1_grau_name.text = ''
        self.ids.compare_box_grau.ids.comp1_uni_name.text = ''
        self.ids.compare_box_grau.ids.comp1_nota.text = ''
        self.ids.compare_box_grau.ids.comp1_places.text = ''
        self.ids.compare_box_grau.ids.comp1_loc.text = ''
        self.ids.compare_box_grau.ids.comp1_rendiment.text = ''
        self.ids.compare_box_grau.ids.comp1_abandonament.text = ''
        self.ids.compare_box_grau.ids.comp1_homes.text = ''
        self.ids.compare_box_grau.ids.comp1_dones.text = ''
        self.ids.compare_box_grau.ids.comp1_credits.text = ''
        self.ids.compare_box_grau.ids.comp1_link.text = ''

        self.ids.compare_box_grau.ids.comp2_grau_name.text = ''
        self.ids.compare_box_grau.ids.comp2_uni_name.text = ''
        self.ids.compare_box_grau.ids.comp2_nota.text = ''
        self.ids.compare_box_grau.ids.comp2_places.text = ''
        self.ids.compare_box_grau.ids.comp2_loc.text = ''
        self.ids.compare_box_grau.ids.comp2_rendiment.text = ''
        self.ids.compare_box_grau.ids.comp2_abandonament.text = ''
        self.ids.compare_box_grau.ids.comp2_homes.text = ''
        self.ids.compare_box_grau.ids.comp2_dones.text = ''
        self.ids.compare_box_grau.ids.comp2_credits.text = ''
        self.ids.compare_box_grau.ids.comp2_link.text = ''

        #UNI
        self.uni_screen.ids.compare_box_uni.ids.comp1_grau_name.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_uni_name.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_nota.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_places.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_loc.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_rendiment.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_abandonament.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_homes.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_dones.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_credits.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp1_link.text = ''

        self.uni_screen.ids.compare_box_uni.ids.comp2_grau_name.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_uni_name.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_nota.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_places.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_loc.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_rendiment.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_abandonament.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_homes.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_dones.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_credits.text = ''
        self.uni_screen.ids.compare_box_uni.ids.comp2_link.text = ''

    def hyperlink(self, link, instance = None):
        webbrowser.open(link)
