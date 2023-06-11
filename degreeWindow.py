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
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

panel_detail = ["""El món de la comunicació digital es basa en la informática, en les xarxes de telecomunicacions i en
altres matèries bâsiques (les matemâtiques, la física, etc.), i especialment en els seus aspectes innovadors, com els relacionats amb les aplicacions més avançades d'Internet. Aquesta és la base dels estudis: una manera moderna i innovadora d'utilitzar les eines bâsiques, aplicada als multimèdia.
El grau en Enginveria en Informâtica proporciona, d'una banda, una formació fonamental i sòlida en informâtica que capacita per a l'exercici de la professió i, d'una altra banda, té una orientació cap a la comunicació digital, que posibilita cursar itineraris optatius centrats en sistemes audiovisuals, comunicacions i continguts
multimèdia, sistemes intel ligents, i xarxes i serveis telemàtics.
El que es proposa és, dones, una formació sòlida, amb innovacions, i una formació aplicada als nous continguts multimedia, laudiovisual digital i els serveis telemátics.
Els graduats en Enginveria en Informática per la UPF
adquireixen al llarg dels seus estudis competêncies generals i específiques. Les competêncies generals o transversals enriqueixen la personalitat i es poden aplicar profitosament a la vida profesional en qualsevol
àmbit social o econòmic. Aquestes inclouen l'expressió oral i escrita, tant en català i en castellà com en anglès, i capaciten els graduats per treballar en equips interdisciplinaris, i també per treballar autônomament, amb una clara motivació per la qualitat.
Les competències especifiques adquirides pels nostres
graduats, que són necessàries per desenvolupar activitats en un entorn tecnològic i empresarial, els permetran tenir una sòlida comprensió de les tecnologies actuals i adaptar-se a les futures tecnologies, competência aquesta que resulta esencial en un entorn tan canviant com és el sector tecnològic.""",
                """• Direcció, anâlisi, dissenv i implementació de tot tipus d'aplicacions informátiques.
• Desenvolupament d'aplicacions web i multimèdia.
• Analisi, dissenv i administració de bases de dades.
• Direcció de projectes de programari i maquinari.
• Instal lació, configuració, administració i manteniment de sistemes informâtics, sistemes operatius i xarxes.
• Disseny i administració de sistemes de comunicacions.
• Disseny, manteniment i actualització d'equips automátics i robotitzats.""",
                """• 0.2
    • Matematiques
    • Matematiques (ciêncies socials )
    • Física
    • Química
    • Matematiques
    • Matematiques (ciêncies socials )
    • Física
    • Química
    • Matematiques
    • Matematiques (ciêncies socials )
    • Física
    • Química
• 0.1
    • Biologia
    • Filosofia"""
                ]


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
    pass


class DegreeWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.courses = {}
        self.selected_course = None
        self.app = MDApp.get_running_app()
        self.conn = self.app.connect_bbdd()
        self.grau_ID = None
        self.uni_ID = None
        self.uni_name = None
        self.queries = aiosql.from_path('sql/queries.sql', 'pymysql')


    def on_pre_enter(self, *args):
        panel = self.ids.panel
        panel.clear_widgets()
        panels_list = ['Descripció del grau', 'Sortides laborals', 'Ponderacions']

        for cnt, i in enumerate(panels_list):
            md_panel = MDExpansionPanel(content=ContentBox(),
                                        panel_cls=MDExpansionPanelOneLine(text=i))
            md_panel.content.ids.panel_text.text = panel_detail[cnt]
            panel.add_widget(md_panel)

        md_panel = MDExpansionPanel(content=IndicatorsBox(), panel_cls=MDExpansionPanelOneLine(text='Indicadors'))
        panel.add_widget(md_panel)
        self.ids.courses_layout.clear_widgets()
        self.ids.bottom_navigation.switch_tab('info')
        self.ids.bottom_navigation.ids.tab_manager.transition = NoTransition()
        self.courses_buttons = []
        self.subjects_buttons = []
        self.add_cursos()
        uni_screen = self.manager.get_screen("uni")
        self.grau_ID = uni_screen.get_selected_grau()
        home_screen = self.manager.get_screen("home")
        self.uni_ID = home_screen.get_selected_uni()
        self.ids.compare_icon.badge_icon = 'numeric-' + str(len(self.app.comparation_degrees))

        if self.uni_ID == 1:
            self.uni_name = 'upf'
        elif self.uni_ID == 2:
            self.uni_name = 'upc'

        uni_grau = self.queries.get_uni_grau_names(self.conn, grau_ID=self.grau_ID, uni_ID=self.uni_ID)
        uni_grau = list(uni_grau)
        print(list(uni_grau))
        if len(uni_grau) > 0:
            self.ids.path.text = f'{uni_grau[0][0]} > {uni_grau[0][1]}'

        # accessing Compare Screen 2nd degree name label text
        print(self.ids.compare_box.ids.s_degree_name.text)

    def update_selected_course(self, course):
        self.selected_course = course

    def add_cursos(self):
        courses = ['1r curs', '2n curs', '3r curs', '4t curs']  # TODO: change, there are degrees longer than 4 years
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
        assignatures = self.queries.get_assignatures(self.conn, grau_ID=self.grau_ID, curs=chosen_curs.number + 1)
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
        self.app.comparation_degrees.append(self.grau_ID)
        self.ids.compare_icon.badge_icon = 'numeric-' + str(int(self.ids.compare_icon.badge_icon.split('-')[1]) + 1)

    def hyperlink(self, link):
        webbrowser.open(link)
