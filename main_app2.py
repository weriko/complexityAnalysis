import requests
import uuid
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
import requests
from kivy.uix.label import Label
import time
import json
from kivy.uix.floatlayout import FloatLayout
import base64
import re
from io import StringIO,BytesIO
import dis
import matplotlib.pyplot as plt
from kivy.uix.image import Image as kvImage, AsyncImage,CoreImage


class Container(FloatLayout):
    def __init__(self,*args,**kwargs):
        
        super(Container,self).__init__(*args,**kwargs)
        self.main_screen()
        self.code = ""
    def main_screen(self):
        self.clear_widgets()
        self.load_btn =Button(text="Load",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.75})
        
        self.load_btn.bind(on_press=self.load_pop_up)
        
        self.add_widget(self.load_btn)
        self.analysis_btn =Button(text="Analysis",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.53})
        self.analysis_btn.bind(on_press=self.main_analysis)
        
        
        
        self.add_widget(self.analysis_btn)
        self.graph_btn =Button(text="Graph",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.31})
        self.add_widget(self.graph_btn)
        
        self.logo_btn =Button(text="IMAGE PLACEHOLDER",
                    
                              size_hint =(.7, .2),
                              pos_hint={"right":0.75,"top":.98})
        self.add_widget(self.logo_btn)
        self.dropdown_btn =Button(text="MENU",
                    
                              size_hint =(.2, .2),
                              pos_hint={"right":0.95,"top":.98})
        self.add_widget(self.dropdown_btn)
        
        self.scrollable_code = ScrollView(size_hint =(.55, 0.64),
                              pos_hint={"right":0.95,"top":0.75})
        self.grid_widget_code = GridLayout(cols=1,size_hint=(1,None))
        self.grid_widget_code.bind(minimum_height=self.grid_widget_code.setter('height'))
        
        self.scrollable_code.add_widget(self.grid_widget_code)
        self.add_widget(self.scrollable_code)
        
        
       
            
        
    def load_pop_up(self,k):
        show = GridLayout(cols=1)
        btn_github = Button(text="Load from Github"
                      )
        
        btn_github.bind(on_press= self.load_github)
        self.github_code_rd = TextInput(text="Link a raw de github",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1))
        
        btn = Button(text="Volver",
                      )
        btn.bind(on_press=lambda x: self.answers_popup.dismiss())
        btn_path_load= Button(text="Load from Path"
                      )
        
        btn_path_load.bind(on_press= self.load_path)
        self.path_code_rd = TextInput(text="Path",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1))
        
        
        show.add_widget(self.github_code_rd)
        show.add_widget(btn_github)
        show.add_widget(self.path_code_rd)
        show.add_widget(btn_path_load)
        show.add_widget(btn)
        self.answers_popup = Popup(title="Resultados",content=show)
        self.answers_popup.open()
        
        
        
        
    def load_github(self,instance):
        try:
            url = self.github_code_rd.text
            rq = requests.get(url)
            if rq.status_code == requests.codes.ok:
                content = rq.content.decode()
                # req is now a dict with keys: name, encoding, url, size ...
                # and content. But it is encoded with base64.
                
            else:
                print('Content was not found.')
            self.code = content
            self.grid_widget_code.clear_widgets()
            for i in self.code.split("\n"):
                self.grid_widget_code.add_widget(TextInput(text=str(i),size_hint_y=None,
                                                           foreground_color=(1,1,1,1),
                                                           background_color= (0,0,0,1)))
            self.answers_popup.dismiss()
        except:
            self.answers_popup.dismiss()
            
    def load_path(self,instance):
        try:
            content = open(self.path_code_rd.text).read()
            self.code = content
            self.grid_widget_code.clear_widgets()
            for i in self.code.split("\n"):
                self.grid_widget_code.add_widget(TextInput(text=str(i),size_hint_y=None,
                                                           foreground_color=(1,1,1,1),
                                                           background_color= (0,0,0,1)))
            self.answers_popup.dismiss()
        except:
            self.answers_popup.dismiss()
            
            


    def get_instructions(self):
        with StringIO() as out:
            dis.dis(self.code,file=out)
            datatemp = out.getvalue()
         
            data = datatemp.split("\n")
        self.code_data = [list(re.split(r'\s{3,}',x)) for x in data]
        self.code_instructions = [x[10:] for x in data]
        #print(self.code_instructions)
        return datatemp
    def get_loops(self):
   
        mx = 0
        curr = 0
        for i in self.code_instructions:
            if "SETUP_LOOP" in i:
                curr+=1
            if "JUMP_ABSOLUTE" in i:
                if curr>mx:
                    mx=curr
                curr= 0
        return mx
               #C:/Users/Santiago/Desktop/Uni/4 semestre/Algoritmos/bunzei/supertemp.py
            
        
    def main_analysis(self,k):
        
        self.clear_widgets()
        self.scrollable_dis = ScrollView(size_hint =(.55, 0.9),
                              pos_hint={"right":0.98,"top":0.95})
        self.grid_widget_dis = GridLayout(cols=1,size_hint=(1,None))
        self.grid_widget_dis.bind(minimum_height=self.grid_widget_dis.setter('height'))
        
        self.scrollable_dis.add_widget(self.grid_widget_dis)
        self.add_widget(self.scrollable_dis)
        datatemp = self.get_instructions()
        for i in datatemp.split("\n"):
                self.grid_widget_dis.add_widget(TextInput(text=str(i),size_hint_y=None,
                                                           foreground_color=(1,1,1,1),
                                                           background_color= (0,0,0,1)))
        cmplx = self.get_loops()
        self.complexity_output =  TextInput(text=str("n^"+str(cmplx)),
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1),
                                                       size_hint=(0.1,0.05),
                                                       pos_hint={"right":0.36,"top":0.95})
        self.add_widget(self.complexity_output)
        x = list(range(0,400))
        y,x = zip(*[((i/10)**float(cmplx),i/10) for i in x])
        
        print(cmplx)
        plt.plot(x,y)
        plt.ylabel("hmm")
        
        
        plt.savefig("temp.jpg")
        
        plt.close()
        self.aimg = kvImage(
                         size_hint=(0.25,0.5),
 
                         pos_hint={"right":0.3,"top":0.92} )
        self.aimg.source = "temp.jpg"
        self.aimg.reload()
        
        self.go_back_btn = Button(text="Back",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.16,"top":.2})
        
        self.go_back_btn.bind(on_press=lambda x : self.main_screen())
        self.add_widget(self.go_back_btn)
        self.add_widget(self.aimg)
        
     
            
            
     
        
        
        
        
class Main(App):
    def build(self):
        return Container()
Window.size=(1000,1000)
Main().run()
Main.get_running_app().stop()