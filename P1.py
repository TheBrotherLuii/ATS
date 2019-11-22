import numpy as np
import matplotlib.pyplot as plt

from sympy import Eq
from sympy.geometry import Point, Circle, Line

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

        TPP = Point(float(self.TP_X.text),float(self.TP_Y.text))

        LM1P = Point(float(self.LM1_X.text),float(self.LM1_Y.text))
        LM2P = Point(float(self.LM2_X.text),float(self.LM2_Y.text))
        LM3P = Point(float(self.LM3_X.text),float(self.LM3_Y.text))

        TPAngLM1 = self.AngleCalc(TPP,LM1P)
        TPAngLM2 = self.AngleCalc(TPP,LM2P)
        TPAngLM3 = self.AngleCalc(TPP,LM3P)

        u, v = np.meshgrid(np.arange(-7, 8, 1), np.arange(-7, 8, 1))
        self.QuiverPlot(u, v)

    def InterPointCalc(self,CurrentPoint,LMP):   
        LM= Circle(LMP,1) 
        return Circle(CurrentPoint,CurrentPoint.distance(LMP)).intersection(LM)
         

    def AngleCalc(self,CP,LMP):
        Xline = Line (CP, (1,0))
        INPoints = self.InterPointCalc(CP,LMP) 

        ln1=Line(CP,INPoints[0])
        angle1= Xline.smallest_angle_between(ln1)

        ln2=Line(CP,INPoints[1])
        angle2 = Xline.smallest_angle_between(ln2)

        HLn = Line(CP,LMP)
        HalfAngle = Xline.smallest_angle_between(HLn)

        if  INPoints[0].args[1]<0:
          angle1 = angle1 * -1
                    
        if  INPoints[1].args[1]<0:
            angle2 = angle2 * -1

        anglesice = ln1.smallest_angle_between(ln2)
        return [anglesice, HalfAngle]

    def QuiverPlot(self,u,v):
        # Create quiver figure
        fig, ax = plt.subplots()
        ax.axis([-7, 7, -7, 7])

        x, y = np.meshgrid(np.arange(-7, 8, 1), np.arange(-7, 8, 1))

        ax.quiver(x,y,u,v,angles='xy', scale_units='xy', scale=1)

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

