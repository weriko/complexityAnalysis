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
import os
import time
import json
from math import log,inf
from kivy.uix.floatlayout import FloatLayout
import base64
import sys
import re
from io import StringIO,BytesIO
import dis
import matplotlib.pyplot as plt
from kivy.uix.image import Image as kvImage, AsyncImage,CoreImage
import ctypes
from kivy.clock import Clock
import contextlib
import ssl






"""
Ver: Beta 0.5
https://github.com/weriko/complexityAnalysis
News:
    
    Added terminal
    Improved stability
    Improved UI
    
TODO:
    Optimize code
    Add screen manager 
    
    
    
"""




ssl._create_default_https_context = ssl._create_unverified_context

try:
    import webbrowser
except:
    pass

try:
    user32 = ctypes.windll.user32
    screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    screensize = (int(screensize[1]/1.5),int(screensize[0]/2.5))
    print(screensize)
  
except:
    try:
        screensize = Window.size
    except:
        screensize = (1600,800)
        
        
class CTextInput(TextInput):
    def _hide_cut_copy_paste(self, win=None):
        if not self._bubble:
            return
        Clock.schedule_once(lambda x: self._bubble.hide() ,2)
        
        
        
Window.keyboard_anim_args= {"d":.2,"t":"in_out_expo"}
Window.softinput_mode = "below_target"

class Container(FloatLayout):
    def __init__(self,*args,**kwargs):
        
        super(Container,self).__init__(*args,**kwargs)
        self.main_screen()
        self.code = ""
        self.function_dict = {}
    def main_screen(self):
        self.main_grid=GridLayout(cols=1,
                              size_hint =(.3, .7),
                              pos_hint={"right":0.32,"top":.75})
        self.clear_widgets()
        self.load_btn =Button(text="Load",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.75})
        
        self.load_btn.bind(on_press=self.load_pop_up)
        
        self.main_grid.add_widget(self.load_btn)
        self.analysis_btn =Button(text="Analysis",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.53})
        self.analysis_btn.bind(on_press=self.main_analysis)
        
        
        
        self.main_grid.add_widget(self.analysis_btn)
        
        
        self.recursive_analysis_btn =Button(text="Recursive\nAnalysis",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.53})
        self.recursive_analysis_btn.bind(on_press=self.main_recursive_analysis)
        
        
        
        self.main_grid.add_widget(self.recursive_analysis_btn)
        
        
        
        
        self.graph_btn =Button(text="Function\nTest",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.31})
        self.graph_btn.bind(on_press=self.graph_pop_up)
        
        self.main_grid.add_widget(self.graph_btn)
        
        self.terminal_btn =Button(text="Terminal",
                    
                              size_hint =(.3, .2),
                              pos_hint={"right":0.32,"top":.31})
        self.terminal_btn.bind(on_press=self.main_terminal)
        
        self.main_grid.add_widget(self.terminal_btn)
        
        self.add_widget(self.main_grid)
        try:
            g_logo_path = "https://github.com//weriko/complexityAnalysis/raw/master/Logo.PNG"
            
            self.logo_btn =AsyncImage(source=g_logo_path,
                        
                                  size_hint =(.7, .2),
                                  pos_hint={"right":0.75,"top":.98})
            self.add_widget(self.logo_btn)
        except:
        	
            try:
                self.logo_btn = kvImage(
    		                 
    	 
    		                pos_hint={"right":0.75,"top":.98} ,
    		                allow_stretch= True,
    		                keep_ratio= True,
    		                size_hint =(.7, .2))
    		                
                self.logo_btn.source = "data/Logo.png"
                self.logo_btn.reload()
                self.add_widget(self.logo_btn)
            except Exception as e:
                print(e)
                                  
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
        
        try:
            if self.code:
                for i in self.code.split("\n"):
                    self.grid_widget_code.add_widget(TextInput(text=str(i),size_hint_y=None,
                                                               readonly=True,
                                                               foreground_color=(1,1,1,1),
                                                               background_color= (0,0,0,1)))
        except:
            pass
        
        
    def run_terminal(self,k): #Executes the code inside terminal
        
        try:
            
            self.terminal_output.foreground_color = (0,0,0,1)
            f = open("console.out","w")
            sys.stdout = f
           
            exec(self.terminal_input.text, locals())
            sys.stdout = sys.__stdout__
            f.close()
            
            out = open("console.out","r").read()
            
            self.terminal_output.text += out
        except Exception as e:
            
            """
            show = Label(text="Please check your code!")
            popup = Popup(title='Menu',
                        content=show,
                        size_hint=(None, None), size=(int(screensize[1]/1.5),int(screensize[0]/1.5)))
            """
            self.terminal_output.text+=f"ERROR\nPlease check your code!\n{e}\n"
            self.terminal_output.foreground_color = (1,0,0,1)
     
    
        
        
                
             
                
            
    def open_terminal_code_run(self,popup):
        try:
            f = open(f"savefiles/{self.open_code_name_input.text}","r")
            self.terminal_input.text = f.read()
            f.close()
            popup.dismiss()
        except:
            self.terminal_output.text+="File not found\n"
            popup.dismiss()
            
        
    def open_terminal_code(self,k):
        
        show =  GridLayout(cols=1)
        self.open_code_name_input = TextInput(text="Untitled.py")
        popup = Popup(title='Save',
                    content=show,
                    size_hint=(None, None), size=(int(screensize[1]/2.5),int(screensize[0]/1.5)))
        open_code_btn =Button(text="""Open""",
                    
                              size_hint =(.2, .2),
                        
                              pos_hint={"right":0.55,"top":.25})
        open_code_btn.bind(on_press= lambda x : self.open_terminal_code_run(popup))
        
        show.add_widget(self.open_code_name_input)
        
        show.add_widget(open_code_btn)
        
        
        popup.open()
        
    def save_terminal_code_run(self,popup):
        try:
            os.mkdir("savefiles")
        except:
            pass
        f = open(f"savefiles/{self.save_code_name_input.text}","w")
        f.write(self.terminal_input.text)
        f.close()
        popup.dismiss()
            
        
    def save_terminal_code(self,k):
        
        show =  GridLayout(cols=1)
        self.save_code_name_input = TextInput(text="Untitled.py")
        save_code_btn =Button(text="""Save""",
                    
                              size_hint =(.2, .2),
                        
                              pos_hint={"right":0.55,"top":.25})
        popup = Popup(title='Save',
                    content=show,
                    size_hint=(None, None), size=(int(screensize[1]/2.5),int(screensize[0]/1.5)))
        save_code_btn.bind(on_press= lambda x: self.save_terminal_code_run(popup))
        
        show.add_widget(self.save_code_name_input)
        
        show.add_widget(save_code_btn)
        
        
        popup.open()
        
    def export_terminal_analysis(self):
        self.code = self.terminal_input.text
        self.main_screen()
        
    def open_github_terminal_code_run(self,popup):
        try:
            url = self.open_github_code_name_input.text
            rq = requests.get(url)
            if rq.status_code == requests.codes.ok:
                content = rq.content.decode()
     
                
            else:
                print('Content was not found.')
            self.terminal_input.text = content
            popup.dismiss()
           
        except:
            self.terminal_output.text += "ERROR\nFile not found"
            popup.dismiss()
            
    def open_github_terminal_code(self,k):
        
        show =  GridLayout(cols=1)
        self.open_github_code_name_input = CTextInput(text="Raw")
        open_github_code_btn =Button(text="""Open""",
                    
                              size_hint =(.2, .2),
                        
                              pos_hint={"right":0.55,"top":.25})
        popup = Popup(title='Save',
                    content=show,
                    size_hint=(None, None), size=(int(screensize[1]/2.5),int(screensize[0]/1.5)))
        open_github_code_btn.bind(on_press=lambda x : self.open_github_terminal_code_run(popup))
        
        show.add_widget(self.open_github_code_name_input)
        
        show.add_widget(open_github_code_btn)
        
        
        popup.open()
                
    def main_terminal(self,k):
        self.clear_widgets()
        run_btn = Button(text="""Run""",
                    
                              size_hint =(.15, .15),
                          
                              pos_hint={"right":0.945,"top":.25})
        
        run_btn.bind(on_press=self.run_terminal)
        
        open_btn =  Button(text="""Open""",
                    
                              size_hint =(.15, .15),
                         
                              pos_hint={"right":0.795,"top":.25})
        open_btn.bind(on_press=self.open_terminal_code)
        
        open_btn_github =  Button(text="""Open\ngithub""",
                    
                              size_hint =(.15, .15),
                         
                              pos_hint={"right":0.345,"top":.25})
        open_btn_github.bind(on_press=self.open_github_terminal_code)
        
        save_btn =  Button(text="""Save""",
                    
                              size_hint =(.15, .15),
                        
                              pos_hint={"right":0.645,"top":.25})
        save_btn.bind(on_press=self.save_terminal_code)
        
        analyze_btn= Button(text="""Analyze""",
                    
                              size_hint =(.15, .15),
                        
                              pos_hint={"right":0.495,"top":.25})
        analyze_btn.bind(on_press=lambda x :self.export_terminal_analysis())
        
        back_btn= Button(text="""Back""",
                    
                              size_hint =(.15, .15),
                        
                              pos_hint={"right":0.195,"top":.25})
        back_btn.bind(on_press=lambda x :self.main_screen())
        
        try:
            a = self.terminal_input.text
        except:
            
            self.terminal_input = CTextInput(text="",
                                        size_hint =(.87, .50),
                            
                                  pos_hint={"right":0.93,"top":.98})
            self.terminal_output = CTextInput(text="",
                                        size_hint =(.87, .20),
                            
                                  pos_hint={"right":0.93,"top":.48})
        self.add_widget(self.terminal_output)
        self.add_widget(self.terminal_input)
        
        self.add_widget(analyze_btn)
        self.add_widget(run_btn)
        self.add_widget(open_btn_github)
        self.add_widget(open_btn)
        self.add_widget(save_btn)
        self.add_widget(back_btn)
        
        
        
    def recursive_function(self,func):
        func=func.text
       
        index = self.functions.index(func)
        print(index)
        
       
        #print(self.functions_helper[index])
        exec(self.functions_helper[index], locals())
        
        times = []
        
        complexity = self.analyze_recursion(self.functions_helper[index])
        for n in range(1,101):
            times.append(eval(complexity[0]  + "* n**"+str(complexity[1])))
          
            
        plt.plot(range(1,101),times)
        plt.ylabel("Time")
        
        
        plt.savefig("temp.png")
        
        plt.close()
        
        self.aimg2.source = "temp.png"
        self.aimg2.reload()
        
        
    def main_recursive_analysis(self,k):
        self.clear_widgets()
        self.scrollable_numeric = ScrollView(size_hint =(.96, 0.45),
                              pos_hint={"right":0.98,"top":0.48})
        show = GridLayout(cols=2,size_hint_y=None)
        show.bind(minimum_height=show.setter('height'))
        self.test_functions() 
       
        self.function_texts = []
        
        
        for i in self.functions:
         
            btn = Button(text=str(i), size_hint_y=None, height=screensize[1]/4,
                      )
            
            btn.bind(on_press=self.recursive_function)
            show.add_widget(btn)
            
            
            
            
            self.function_texts.append(i)
       
        
        
        self.aimg2 = kvImage(
                     
 
                     pos_hint={"right":0.95,"top":0.96} ,
                     allow_stretch= True,
                    keep_ratio= True,
                    size_hint_y=.45,
                    size_hint_x= .9)
        self.add_widget(self.aimg2)
            
     
        btn2 = Button(text="Back",size_hint_y=None,height=screensize[1]/4,
                      )
        btn2.bind(on_press=lambda x: self.main_screen())
        
        
        
        self.scrollable_numeric.add_widget(show)
        show.add_widget(btn2)
        self.add_widget(self.scrollable_numeric)
        
    def exec_function(self,func):
        index = self.functions.index(func.text)
        #print(index)
        print(index)
        print(self.functions_helper)
        print(len(self.functions_helper))
        function_def = self.functions_helper[index]
        try:
     
            func=func.text
            #print(self.functions)
            #print(self.functions_helper)
            
            
            
      
            
            print(function_def)
            #print(self.functions_helper[index])
            function_name = self.get_function_name(self.functions[index])
            function_name = function_name[:function_name.index("(")]
            #function_name = f"global {function_name}\n" + function_def
            
            print(function_name)
            exec(function_def, locals())
            
            times = []
            rng = self.function_range[index].text.split(",")
            function = self.function_texts[index].text.replace("x","i")
           
            
            
            
            for i in range(int(rng[0]),int(rng[1]),int(rng[2])):
                s = time.time()
                
                exec(function, locals())
                times.append(time.time()-s)
                
                
            plt.plot(range(int(rng[0]),int(rng[1]),int(rng[2])),times)
            plt.ylabel("Time")
            
            
            plt.savefig("temp.png")
            
            plt.close()
            
            self.aimg2.source = "temp.png"
            self.aimg2.reload()
        except Exception as e:
            #print(e)
            show = GridLayout(cols=1)
            label = Label(text="ERROR\nCheck your range input\nOnly x can be a non constant argument!\n--> f(x,5,3)\nIt is possible for max recursion depth\nto be reached")
            popup = Popup(title='Menu',
                        content=show,
                        size_hint=(None, None), size=(int(screensize[1]/2.5),int(screensize[0]/1.5)))
            
            show.add_widget(label)
         
            popup.open()
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
        size_hint=(None, None), size=(int(screensize[1]/2.5),int(screensize[0]/1.5)))
        self.help_popup.open() 
    def open_browser_help(self,k):
        try:
            webbrowser.open('https://github.com/weriko/complexityAnalysis/blob/master/guiaEN.pdf', new=2)
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
        self.help_popup.size=(int(screensize[1]/2.5),int(screensize[0]/1.5))
        
        
        
    def graph_help(self,k):
        show = GridLayout(cols=1)
        help_label = TextInput(text="""Input:\n
                           First field -> name_of_function(x,args). There can only be one argument varying, and that should be x. Every other argument should be a constant\n
                           Second field -> START,END,STEP  ,The range in which x will be tested""")
        back_button = Button(text="back")
        self.graph_help_popup = Popup(title='Menu',
        content=show,
        size_hint=(None, None), size=(int(screensize[1]/2.5),int(screensize[0]/1.5)))
        show.add_widget(help_label)
        show.add_widget(back_button)
        back_button.bind(on_press=self.graph_help_popup.dismiss)
        
        
        self.graph_help_popup.open() 
      
        
        
    def graph_pop_up(self,k):
        self.clear_widgets()
        self.scrollable_numeric = ScrollView(size_hint =(.96, 0.45),
                              pos_hint={"right":0.98,"top":0.48})
        show = GridLayout(cols=3,size_hint_y=None)
        show.bind(minimum_height=show.setter('height'))
        
        self.test_functions()
       
        self.function_texts = []
        self.function_range = []
        
        for i in self.functions:
         
            btn = Button(text=str(i),size_hint_y=None,height=screensize[1]/4
                      )
            
            btn.bind(on_press=self.exec_function)
            show.add_widget(btn)
            
            
            temp = TextInput(text=self.get_function_name(str(i)),size_hint_y=None,
            						height=screensize[1]/4,
                                                     foreground_color=(1,1,1,1),
                                                     background_color= (0,0,0,1))
            temp2 = TextInput(text="0,10,1",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                       height=screensize[1]/4,
                                                     background_color= (0,0,0,1))
            self.function_texts.append(temp)
            self.function_range.append(temp2)
            show.add_widget(temp)
            show.add_widget(temp2)
        btn = Button(text="Help",size_hint_y=None,height=screensize[1]/4,
                     
                     
                      )
            
        btn.bind(on_press=self.graph_help)
        show.add_widget(btn)
        self.aimg2 = kvImage(
                     
 
                     pos_hint={"right":0.95,"top":0.96} ,
                     allow_stretch= True,
                    keep_ratio= True,
                    size_hint_y=.45,
                    size_hint_x= .9)
        self.add_widget(self.aimg2)
            
     
        btn2 = Button(text="Back",size_hint_y=None,height=screensize[1]/4,
                      )
        btn2.bind(on_press=lambda x: self.main_screen())
      
        
        
        
        show.add_widget(btn2)
        
        self.scrollable_numeric.add_widget(show)
        self.add_widget(self.scrollable_numeric)
        #self.answers_popup = Popup(title="Resultados",content=show)
        #self.answers_popup.open()        
        
    def delete_input_text(self,k,p):
        
        deleatable_list = ["Raw github link", "Path"]
        if k.text in deleatable_list:
            k.text = ""
            
        
    def load_pop_up(self,k):
        show = GridLayout(cols=1)
        btn_github = Button(text="Load from Github"
                      )
        
        btn_github.bind(on_press= self.load_github)
        self.github_code_rd = CTextInput(text="Raw github link",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1))
        self.github_code_rd.bind(on_touch_down=self.delete_input_text)
        
        btn = Button(text="Back",
                      )
        btn.bind(on_press=lambda x: self.answers_popup.dismiss())
        btn_path_load= Button(text="Load from Path"
                      )
        
        btn_path_load.bind(on_press= self.load_path)
        self.path_code_rd = CTextInput(text="Path",size_hint_y=None,
                                                       foreground_color=(1,1,1,1),
                                                       background_color= (0,0,0,1))
        self.path_code_rd.bind(on_touch_down=self.delete_input_text)
        
        
        show.add_widget(self.github_code_rd)
        show.add_widget(btn_github)
        show.add_widget(self.path_code_rd)
        show.add_widget(btn_path_load)
        show.add_widget(btn)
        self.answers_popup = Popup(title="Resultados",content=show)
        self.answers_popup.open()
        
    def get_tabs(self,line):
        tabs=0
        for i in line:
            if i==" ":
                tabs+=1
            else:
                break
        return tabs
    
    def check_alpha(self,x):
        for i in x:
            
            if i.isalnum():
                return True
        return False
    
    def get_function_name(self,function):
        for i in function.split("\n"):
            if "def" in i:
                func_name=i
                break
 
        func_name = func_name.split(" ")[1]
        return func_name.replace(":","")
        
    def get_functions(self):
        func_tabs = 0
        func = []
        total_func = []
        for line in self.code.split("\n"):
            if "def" in line and self.get_tabs(line)<=func_tabs:
                if func != []: # If func is not an empty list, append to total_func
                    total_func.append(func)
                func = [line] #Starts the list with the current line
                func_tabs = self.get_tabs(line) #this is the amount of lines in the definition of funtion
                continue #If it finds a def, it gets all the lines inside the def
            if self.get_tabs(line)>func_tabs or (lambda s: any([c.isalnum() for c in s], line)):
                func.append(line) #If the number of indentations is higher than the definition, it adds the line to the list, othewise it stops
            else:
                total_func.append(func)
                func = []
        if func!=[]:
            total_func.append(func)
        return list(filter (lambda s:any([self.check_alpha(c) for c in s]), total_func))
    
    
    
    def analyze_recursion_helper(self,line,func_name):
        if "(" not in line:
            return 0
        op=0
        flag=0
        counter = 0
        helper=[]
  
        for i in range(len(line)):
        
            if line[i]=="(":
                op+=1
                start=i
                flag=1
            if line[i]==")":
                op-=1
            if op==0 and flag:
                helper.append((start,counter))
                op=0
                flag=0
                counter=0
            if op!=0:
                counter+=1
        #print(helper)
        a = len(helper)
        b_list = []
        for i in [line[x[0]:x[0]+x[1]] for x in helper]:
            #print(i)
            temp = ""
            
            for j in i:
          
                if j.isdigit():
                    temp+=j
                else:
                    b_list.append(temp)
                    temp=""
            b_list.append(temp)
                
                        
          
        
     
        try:
            b = max([int(x) for x in b_list if x.isdigit()])
        except:
            b=0
      
        if a>=1 and b==0:
            return "inf"
        elif a>=2:
            return f"{a}**n"
        elif a==0:
            return "1"
        elif a == b and "/" in line and b!=1:
            return f"n*log(n)" 
        elif "/" in line:
            return f"log(n)"
        
        else:
            return f"n" 
            
        
        
    def analyze_recursion(self, function):
        
        for i in function.split("\n"):
            if "def" in i:
                func_name=i
                break
 
        func_name = func_name.split(" ")[1]
        string = ""
        for i in func_name:
            if i !="(":
                string+=i
            else:
                
                break
        func_lines = [x for x in function.split("\n") if string in x]
        complexities = []
        for i in func_lines[1:]:
            
            complexities.append(self.analyze_recursion_helper(i,string))
            
        mx = "1"   
        flag=0
        for i in complexities:
            if i=="inf":
                mx="inf"
                break
            if "**n" in str(i):
                mx = i
                flag=3
            if i=="n*log(n)" and flag<3:
                mx=i
                flag=2
            if i=="log(n)" and flag<2:
                mx=i
                flag = 1
            if i=="n":
                mx="n"
        #print(mx)
        loops =   self.get_instructions(code=function)
        loops = self.get_loops(code=loops)
        #print(loops)
        return mx,loops

    
    def test_functions(self):
        
        code = self.code.split("\n")
        self.functions = [x for x in code if "def" in x]     
        
        
        helper_helper = self.get_functions()
        helper_helper_helper = []
        for i in helper_helper:
            #print(i)
            helper_helper_helper.append(["".join(x+"\n") for x in i])
        #print(helper_helper_helper) 
        helper_helper_helper_helper = []
        
       
        self.functions_helper = ["".join(x) for x in helper_helper_helper]
        #print(self.functions_helper,"\naaaa")
        
                
                
                
                
        
        
        
        
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
                                                           readonly=True,
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
                                                           readonly=True,
                                                           foreground_color=(1,1,1,1),
                                                           background_color= (0,0,0,1)))
            self.answers_popup.dismiss()
        except:
            self.answers_popup.dismiss()
            
            


    def get_instructions(self, code = None):
        if code: #If code is passed as an argument, it uses that code instead of the one saved in object variable and returns the instructions for the code passed as argument
             with StringIO() as out:
                dis.dis(code,file=out)
                datatemp = out.getvalue()
             
                data = datatemp.split("\n")
             code_data = [list(re.split(r'\s{3,}',x)) for x in data]
             code_instructions = [x[10:] for x in data]
             #print(self.code_instructions)
             return code_instructions
        
        
        
        with StringIO() as out:
            dis.dis(self.code,file=out)
            datatemp = out.getvalue()
         
            data = datatemp.split("\n")
        self.code_data = [list(re.split(r'\s{3,}',x)) for x in data]
        self.code_instructions = [x[10:] for x in data]
        #print(self.code_instructions)
        return datatemp
    
    
    def get_loops(self, code = None):
        #If code is passed as an argument, it uses that code instead of the one saved in object variable and returns the analysis for the code passed as argument
        mx = 0
        curr = 0
        
        print(sys.version_info)
        op_code = "GET_ITER" if float(sys.version[:3]) >= 3.8 else "SETUP_LOOP"
        #print(op_code)
        
        if code:
            for i in code:
                if op_code in i:
                    curr+=1
                   
                if "JUMP_ABSOLUTE" in i:
                    if curr>mx:
                        mx=curr
                    curr= 0
        else:    
        
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
                                                          readonly=True,
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
        plt.ylabel("Time")
        
        
        plt.savefig("temp.png")
        
        plt.close()
        self.aimg = kvImage(
                         
 
                         pos_hint={"right":0.42,"top":0.92} ,
                         allow_stretch= True,
                        keep_ratio= True,
                        size_hint_y=.6,
                        size_hint_x= .4)
        self.aimg.source = "temp.png"
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
Window.size=screensize
Main().run()
Main.get_running_app().stop()
