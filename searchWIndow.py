from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


class SearchWindow(Screen):
    def on_pre_enter(self, *args):
        data = [['assets/upf_logo_no_writings.png', 'Enginyeria Informática', 'Universitat Pompeu Fabra',
                 '10,154', 'Barcelona'],
                ['assets/upc_icon.png', 'Enginyeria Informática', 'Universitat Politécnica de Catalunya',
                 '10,698', 'Barcelona'],
                ['assets/ub_logo.png', 'Enginyeria Informática', 'Universitat de Barcelona',
                 '10,118', 'Barcelona'],
                ['assets/uab_logo.png', 'Enginyeria Informática', 'Universitat Autònoma de Catalunya',
                 '9,696', 'Cerdanyola'],
                ['assets/udg_logo.png', 'Enginyeria Informática', 'Universitat de Girona',
                 '8,364', 'Girona'],
                ['assets/udl_logo.png', 'Enginyeria Informática', 'Universitat de Lleida',
                 '7,692', 'Lleida']
                 ]
        
        view_area = self.ids.search_area
        view_area.clear_widgets()
        for result in data:
            item = SearchItemCard(icon_left=result[0], uni_name=result[1], sub_title=result[2],
                                  pages=result[3], loc=result[4])

            view_area.add_widget(item)

    def on_t(self):
        print(self.ids.search_field.ids.field.text)

class SearchItemCard(MDCard):
    icon_left = StringProperty()
    uni_name = StringProperty()
    sub_title = StringProperty()
    pages = StringProperty()
    loc = StringProperty()
