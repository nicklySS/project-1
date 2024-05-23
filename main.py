from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard as Cb
import requests
import json

KV = """
MyBL:
        orientation: "vertical"
        size_hint: (0.95, 0.95)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        Label:
                font_size: "15sp"
                multiline: True
                text: root.data_label
                text_size : self.width*0.98, None
                height: self.texture_size[1] + 15
                size_hint_x: 1.0
                size_hint_y: None
                markup: True
                on_ref_press: root.linki()

        TextInput:
                id: Inp
                multiline: False
                padding_y: (5,5)
                size_hint: (1, 0.5)
                on_text: root.inp_text = self.text

        Button:
                text: "Получить комментарии"
                bold: True
                background_color: "#00FFCE"
                size_hint: (1, 0.5)
                on_press: root.callback()
        Button:
                text: "Найти по email"
                bold: True
                background_color: "#00FFCE"
                size_hint: (1, 0.5)
                on_press: root.callback2()
"""


class MyBL(BoxLayout):
    data_label = StringProperty("")
    datas = []
    inp_text = ''

    def callback(self):
                url = "https://jsonplaceholder.typicode.com/comments"
                response = requests.get(url)
                if response.status_code == 200:
                        data = json.loads(response.content)
                        for i in range(len(data)):
                                self.datas.append(data[i])
                        self.data_label = str("Данные получены успешно!")
                        
                else:
                        self.data_label = str("Произошла ошибка при получении данных!")
                        print(f"Ошибка сервера: {response.status_code}")


    def callback2(self):
                if self.datas:
                        for i in range(len(self.datas)):
                                if self.datas[i]['email'] == self.inp_text:
                                        self.emailll = self.inp_text
                                        self.data_label = 'Пользователь с email '+ self.inp_text + ' успешно найден!'
                                        self.data_label += '\n[color=#00FFCE]Имя[/color]: ' + self.datas[i]['name']
                                        self.data_label += '[ref=linki]' + '\n[color=#00FFCE]Почта[/color]: ' + '[color=#ff0000]' + self.datas[i]['email'] + '[/color]' + '[/ref]'
                                        self.data_label += '\n[color=#00FFCE]Комментарий[/color]: ' + self.datas[i]['body']
                                else: 
                                        self.data_label = 'Пользователь с таким email не найден!'
                else:
                        self.data_label = 'Пожалуйста, нажмите кнопку "Получить комментарии"'
    def linki(self):
        Cb.copy(self.emailll)

class MyApp(App):
        

    running = True


    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False

MyApp().run()