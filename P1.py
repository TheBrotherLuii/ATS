import numpy as np
import matplotlib.pyplot as plt

from sympy import *
from sympy.geometry import *


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput


class StartScreen(GridLayout):

    def __init__(self,**kwargs):
        super(StartScreen,self).__init__(**kwargs)
 
        self.cols = 3
        self.add_widget(Label(text='',font_size='20sp'))
        self.add_widget(Label(text='X-Value',font_size='20sp'))
        self.add_widget(Label(text='Y-Value',font_size='20sp'))

        self.add_widget(Label(text='Target Point',font_size='20sp'))
        self.TP_X = TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.TP_X)
        self.TP_Y= TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.TP_Y)

        self.add_widget(Label(text='Landmark 1',font_size='20sp'))
        self.LM1_X = TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.LM1_X)
        self.LM1_Y = TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.LM1_Y)

        self.add_widget(Label(text='Landmark 2',font_size='20sp'))
        self.LM2_X = TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.LM2_X)
        self.LM2_Y= TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.LM2_Y)

        self.add_widget(Label(text='Landmark 3',font_size='20sp'))
        self.LM3_X = TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.LM3_X)
        self.LM3_Y= TextInput(multiline=False,font_size='50sp')
        self.add_widget(self.LM3_Y)

        self.add_widget(Label(text=''))
        DrawButton = Button(text='Draw' ,font_size='60sp',background_color=[0,1,0,1])
        DrawButton.bind(on_press = self.CalculateDrawing)
        self.add_widget(DrawButton)
        self.add_widget(Label(text=''))
    
    def CalculateDrawing(self,instance):

        LM1= Circle(Point(float(self.LM1_X.text),float(self.LM1_Y.text)),1)
        LM2= Circle(Point(float(self.LM2_X.text),float(self.LM2_Y.text)),1)
        LM3= Circle(Point(float(self.LM3_X.text),float(self.LM3_Y.text)),1)

        TPC = Circle((float(self.TP_X.text),float(self.TP_Y.text),TP.canberra_distance(LM1)) 
        InPoint = TPC.intersection(LM1)
        print(InPoint)
        u, v = np.meshgrid(np.arange(-7, 8, 1), np.arange(-7, 8, 1))
        self.QuiverPlot(u, v)

    def QuiverPlot(self,u,v):
        # Create quiver figure
        fig, ax = plt.subplots()
        ax.axis([-7, 7, -7, 7])

        x, y = np.meshgrid(np.arange(-7, 8, 1), np.arange(-7, 8, 1))

        ax.quiver(x, y,u,v,angles='xy', scale_units='xy', scale=1)

        LMX=np.array([float(self.LM1_X.text), float(self.LM2_X.text) ,float(self.LM3_X.text)])
        LMY=np.array([float(self.LM1_Y.text),float(self.LM2_Y.text),float(self.LM3_Y.text)])
        ax.scatter(float(self.TP_X.text),float(self.TP_Y.text),color='r') #Honeypot
        ax.scatter(LMX,LMY,color='g') #Landmarks

        ax.set_title('Honey Way')
        plt.show()

class TestApp(App):
    def build(self):
        return StartScreen()


TestApp().run()

