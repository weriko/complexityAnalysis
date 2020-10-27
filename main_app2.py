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
import re
import requests
from kivy.uix.label import Label
import time
import json
from kivy.uix.floatlayout import FloatLayout
import base64
import sys
import re
from io import StringIO,BytesIO
import dis
import matplotlib.pyplot as plt
from kivy.uix.image import Image as kvImage, AsyncImage,CoreImage
import ctypes
try:
    import webbrowser
except:
    pass

user32 = ctypes.windll.user32
screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
print(screensize)

class Container(FloatLayout):
    def __init__(self,*args,**kwargs):
        
        super(Container,self).__init__(*args,**kwargs)
        self.main_screen()
        self.code = ""
        self.function_dict = {}
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
        self.graph_btn.bind(on_press=self.graph_pop_up)
        try:
            g_logo_path = "https://github.com//weriko/complexityAnalysis/raw/master/Logo.PNG"
            
            self.logo_btn =AsyncImage(source=g_logo_path,
                        
                                  size_hint =(.7, .2),
                                  pos_hint={"right":0.75,"top":.98})
            self.add_widget(self.logo_btn)
        except:
            pass
        self.dropdown_btn =Button(text="""
               __
               __  
               __
                                  """,
                                  font_size=30,
                              size_hint =(.2, .2),
                              background_color=(0,0,0,0),
                              pos_hint={"right":0.95,"top":.98})
        self.add_widget(self.dropdown_btn)
        self.dropdown_btn.bind(on_press=self.help_pop_up)
        
        self.scrollable_code = ScrollView(size_hint =(.55, 0.64),
                              pos_hint={"right":0.95,"top":0.75})
        self.grid_widget_code = GridLayout(cols=1,size_hint=(1,None))
        self.grid_widget_code.bind(minimum_height=self.grid_widget_code.setter('height'))
        
        self.scrollable_code.add_widget(self.grid_widget_code)
        self.add_widget(self.scrollable_code)
        
    def exec_function(self,func):
     
        func=func.text
       
        index = self.functions.index(func)
        
       
        print(self.functions_helper[index])
        exec(self.functions_helper[index])
        
        times = []
        rng = self.function_range[index].text.split(",")
        for i in range(int(rng[0]),int(rng[1]),int(rng[2])):
            s = time.time()
            
            exec(self.function_texts[index].text.replace("x","i"))
            times.append(time.time()-s)
            
            
        plt.plot(range(int(rng[0]),int(rng[1]),int(rng[2])),times)
        plt.ylabel("hmm")
        
        
        plt.savefig("temp.jpg")
        
        plt.close()
        
        self.aimg2.source = "temp.jpg"
        self.aimg2.reload()
        
    def help_pop_up(self,k):
        show = GridLayout(cols=1)
        self.button_about = Button(text="About",
                      )
        self.button_help = Button(text="Help")
        
        show.add_widget(self.button_about)
        show.add_widget(self.button_help) 
        
        self.button_about.bind(on_press=self.load_about_us_pop_up)
        self.button_help.bind(on_press=self.open_browser_help)
        try:
            self.help_popup.dismiss()
        except:
            pass
        self.help_popup = Popup(title='Menu',
        content=show,
        size_hint=(None, None), size=(int(screensize[1]/3.5),int(screensize[0]/5.5)))
        self.help_popup.open() 
    def open_browser_help(self,k):
        try:
            webbrowser.open('https://github.com/weriko/complexityAnalysis/blob/master/TEST.pdf', new=2)
        except:
            
             popup = Popup(title='ERROR', 
                                     content= Label(text="CONNECTION ERROR"))
             popup.open()
            
        
    def load_about_us_pop_up(self,k):
        grid = GridLayout(cols=1)
        about_label = Label(text="https://github.com/weriko\nhttps://github.com/AndresYT",font_size=30)
        button_back = Button(text="back")
        button_back.bind(on_press=self.help_pop_up)
        grid.add_widget(about_label)
        grid.add_widget(button_back)
        self.help_popup.content=grid
        self.help_popup.size=(int(screensize[1]/2.8),int(screensize[0]/5.8))
        
        
        
       
    def graph_pop_up(self,k):
        self.clear_widgets()
        self.scrollable_numeric = ScrollView(size_hint =(.55, 0.9),
                              pos_hint={"right":0.98,"top":0.95})
        show = GridLayout(cols=3)
        self.test_functions()
       
        self.function_texts = []
        self.function_range = []
        
        for i in self.functions:
         
            btn = Button(text=str(i),
                      )
            
            btn.bind(on_press=self.exec_function)
            show.add_widget(btn)
            
            
            temp = TextInput(text=str(i),size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                     background_color= (0,0,0,1))
            temp2 = TextInput(text="Range",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                     background_color= (0,0,0,1))
            self.function_texts.append(temp)
            self.function_range.append(temp2)
            show.add_widget(temp)
            show.add_widget(temp2)
        self.aimg2 = kvImage(
                     
 
                     pos_hint={"right":0.42,"top":0.92} ,
                     allow_stretch= True,
                    keep_ratio= True,
                    size_hint_y=.6,
                    size_hint_x= .4)
        self.add_widget(self.aimg2)
            
     
        btn2 = Button(text="Back",
                      )
        btn2.bind(on_press=lambda x: self.main_screen())
        btn_path_load= Button(text="Load from Path"
                      )
        
        btn_path_load.bind(on_press= self.load_path)
        
        
        
        self.scrollable_numeric.add_widget(show)
        show.add_widget(btn2)
        self.add_widget(self.scrollable_numeric)
        #self.answers_popup = Popup(title="Resultados",content=show)
        #self.answers_popup.open()        
        
    def load_pop_up(self,k):
        show = GridLayout(cols=1)
        btn_github = Button(text="Load from Github"
                      )
        
        btn_github.bind(on_press= self.load_github)
        self.github_code_rd = TextInput(text="Raw github link",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1))
        
        btn = Button(text="Back",
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
    def test_functions(self):
        code = self.code.split("\n")
        self.functions = [x for x in code if "def" in x]     
        indexes = [code.index(x) for x in self.functions]
        counter = 0
        helper = []
        helper_helper = []
        for i in indexes:
            tabs = len([x for x in code[i+1] if x ==" "])
            for j in code[i+1:]:
                if j[:tabs]==" "*tabs:
                    helper.append(j)
                else:
                    break
            helper_helper.append(helper)
            helper = []
        helper_helper_helper = []
        for i in helper_helper:
            #print(i)
            helper_helper_helper.append(["".join(x+"\n") for x in i])
        #print(helper_helper_helper) 
        helper_helper_helper_helper = []
        
        for i in helper_helper_helper:
            helper_helper_helper_helper.append("".join(i))
        self.functions_helper = [self.functions[i]+"\n" + helper_helper_helper_helper[i] for i in range(len(indexes))]
        
        
                
                
                
                
        
        
        
        
    def load_github(self,instance):
        try:
            url = self.github_code_rd.text
            rq = requests.get(url)
            if rq.status_code == requests.codes.ok:
                content = rq.content.decode()
     
                
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
        print(self.code_instructions)
        print(sys.version_info)
        op_code = "GET_ITER" if float(sys.version[:3]) >= 3.8 else "SETUP_LOOP"
        print(op_code)
        
        for i in self.code_instructions:
            if op_code in i:
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
        self.complexity_output =  TextInput(text=str("O(n^"+str(cmplx)+")"),
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1),
                                                       font_size=20,
                                                       size_hint=(0.1,0.05),
                                                       pos_hint={"right":0.3,"top":0.95})
        self.add_widget(self.complexity_output)
        x = list(range(0,1000))
        y,x = zip(*[((i/10)**float(cmplx),i/10) for i in x])
        
        #print(cmplx)
        plt.plot(x,y)
        plt.ylabel("hmm")
        
        
        plt.savefig("temp.jpg")
        
        plt.close()
        self.aimg = kvImage(
                         
 
                         pos_hint={"right":0.42,"top":0.92} ,
                         allow_stretch= True,
                        keep_ratio= True,
                        size_hint_y=.6,
                        size_hint_x= .4)
        self.aimg.source = "temp.jpg"
        self.aimg.reload()
        
        self.go_back_btn = Button(text="Back",
                    
                              size_hint =(.2, .1),
                              pos_hint={"right":0.25,"top":.2})
        
        self.go_back_btn.bind(on_press=lambda x : self.main_screen())
        self.add_widget(self.go_back_btn)
        self.add_widget(self.aimg)
        
     
            
            
     
        
        
        
        
class Main(App):
    def build(self):
        return Container()
Window.size=(int(screensize[1]/1.5),int(screensize[0]/2.5))
Main().run()
Main.get_running_app().stop()