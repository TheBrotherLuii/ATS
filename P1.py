
import numpy as np

import plotly.graph_objects as go
import plotly.figure_factory as ff

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
        self.LM1_Y= TextInput(multiline=False,font_size='50sp')
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
        x,y = np.meshgrid(np.arange(-7, 7, .25), np.arange(-7, 7, .25))

        z = x*np.array(x**2)
        v, u = np.array(z)
        self.QuiverPlot(x, y, u, v)

    def QuiverPlot(self,x, y, u, v):
        # Create quiver figure
        fig = ff.create_quiver(x, y, u, v,
                            scale=.5,
                            arrow_scale=1,
                            name='quiver',
                            line_width=1)

        # Add points to figure
        fig.add_trace(go.Scatter(x=[float(self.LM1_X.text),float(self.LM2_X.text),float(self.LM3_X.text)],
                            y=[float(self.LM1_Y.text),float(self.LM2_Y.text),float(self.LM3_Y.text)],
                            mode='markers',
                            marker_size=30,
                            name='Landmarks'))

        fig.add_trace(go.Scatter(x=[float(self.TP_X.text)],y=[float(self.TP_X.text)],
                            mode='markers',
                            marker_size=10,
                            name='Target Point',
                             ))
        fig.show()
        exit

class TestApp(App):
    def build(self):
        return StartScreen()

TestApp().run()

