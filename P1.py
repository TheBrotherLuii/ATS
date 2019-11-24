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
        #Interface
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
        #setting up LandMark Centers
        self.LM1P = Point(float(self.LM1_X.text),float(self.LM1_Y.text))
        self.LM2P = Point(float(self.LM2_X.text),float(self.LM2_Y.text))
        self.LM3P = Point(float(self.LM3_X.text),float(self.LM3_Y.text))
       
        TPP = Point(float(self.TP_X.text),float(self.TP_Y.text))  #setting up TargetPoint Points
        TPAngleLM, TPAngleEmpty = self.AnglestoLM(TPP)#Angel to LM
        #setting up meshgris -7 to 7
        xx,yy  = np.meshgrid(np.arange(-7, 8, 1),np.arange(-7, 8, 1), indexing='xy')
        for i in range(len(xx)):
            for j in range(len(yy)):
                CP = Point(xx[j,i],yy[j,i]) #Current Loop Point
                SSAngles = self.AnglestoLM(CP) #Snapshot to LM Current Point
                AngleMidx = self.MatchTPAngles(SSAngles,TPAngleLM) #Matching Angles
                

    def MatchTPAngles(self,SSAngles,TPAngles): 
        SSAnglelist= [SSAngles[0][1] , SSAngles[1][1] ,  SSAngles[2][1]]
        for i in range(len(SSAngles)):
            SSAnglelist = np.asarray(SSAnglelist)
            idx = (np.abs(SSAnglelist - TPAngles[i][1])).argmin()

        return idx

    def AnglestoLM(self,CurrentPoint):  
        AngLM1 = self.AngleLMCalc(CurrentPoint,self.LM1P)
        AngLM2 = self.AngleLMCalc(CurrentPoint,self.LM2P)
        AngLM3 = self.AngleLMCalc(CurrentPoint,self.LM3P)
        AngET1 = self.AngleEtCalc(CurrentPoint,AngLM1,AngLM2,AngLM3)

        return [AngLM1,AngLM2,AngLM3], AngET1


    def InterPointCalc(self,CurrentPoint,LMP):   
        LM= Circle(LMP,1) 
        return Circle(CurrentPoint,CurrentPoint.distance(LMP)).intersection(LM)

    def AngleLMCalc(self,CP,LMP):
        Xline = Line (CP, (1,0)) #x-Line
        INPoints = self.InterPointCalc(CP,LMP) #Calculate outside Points of LM from CP
        ln1=Line(CP,INPoints[0])
        Angle1= Xline.smallest_angle_between(ln1) #Angle of 1 LMpoint to X
        ln2=Line(CP,INPoints[1])
        Angle2 = Xline.smallest_angle_between(ln2) #Angle of 2 LMpoint to X


    
        if  INPoints[0].args[1]<0: # if negativ Y angle negativ  
            if  INPoints[0].args[0]>0: # if positiv  X angle positiv
                Angle1 = 2 * np.pi - Angle1
            else:
                Angle1 = Angle1 + np.pi
        elif INPoints[0].args[0]<0: # if negativ  X angle negativ
            Angle1 = np.pi - Angle1

        if  INPoints[1].args[1]<0: # if negativ Y angle negativ  
            if  INPoints[1].args[0]>0: # if positiv  X angle positiv
                Angle2 = 2 * np.pi - Angle2
            else:
                Angle2 = Angle2 + np.pi
        elif INPoints[1].args[0]<0: # if negativ  X angle negativ
            Angle2 = np.pi - Angle2

        SiceAngle,HalfAngle = self.AngleHalfAndSice(Angle1,Angle2) 

        return [SiceAngle,HalfAngle,Angle1,Angle2]

    
    def AngleEtCalc(self,CP,LM1,LM2,LM3): 
        LM = [LM1, LM2 , LM3]

        LM.sort(key=lambda HAng: HAng[1])

        if LM[0][2]>np.pi or LM[0][3]>np.pi:
            if LM[0][2]<LM[0][3]: #liegt auf x achse
                EMPAngle=LM[0][2]
            else:
                EMPAngle=LM[0][3]
        else:
            if LM[0][2]>LM[0][3]: #liegt nicht auf x achse
                EMPAngle=LM[0][2]
            else:
                EMPAngle=LM[0][3]
        
        if LM[1][2]<LM[1][3]: 
            EMPAngle2=LM[1][2]
        else:
            EMPAngle2=LM[1][3]

        SiceAngle = abs(EMPAngle-EMPAngle2) # AngleSice
        HalfAngle = (EMPAngle+EMPAngle2)/2

        EM1 = [SiceAngle,HalfAngle,EMPAngle,EMPAngle2]
        
        if LM[1][2]>LM[1][3]: 
            EMPAngle=LM[1][2]
        else:
            EMPAngle=LM[1][3]

        
        if LM[2][2]<LM[2][3]: 
            EMPAngle2=LM[2][2]
        else:
            EMPAngle2=LM[2][3]

        SiceAngle = abs(EMPAngle-EMPAngle2) # AngleSice
        HalfAngle = (EMPAngle+EMPAngle2)/2
        EM2 = [SiceAngle,HalfAngle,EMPAngle,EMPAngle2]

        if LM[2][2]>LM[2][3]: 
            EMPAngle=LM[2][2]
        else:
            EMPAngle=LM[2][3]

        if LM[0][2]>EMPAngle: #beide groß
            EMPAngle2 = LM[0][2]
            HalfAngle = (EMPAngle2 + EMPAngle)/2
            SiceAngle = EMPAngle2 - EMPAngle
        elif LM[0][3]>EMPAngle:
            EMPAngle2 = LM[0][3]
            HalfAngle = (EMPAngle2 + EMPAngle)/2
            SiceAngle = EMPAngle2 - EMPAngle
        else:
            if LM[0][2]>LM[0][3]: #einer sehr klein
                EMPAngle2=LM[0][3]
                SiceAngle = EMPAngle2 + 2 * np.pi - EMPAngle
                HalfAngle = EMPAngle2 + SiceAngle/2
            else:
                EMPAngle2=LM[0][2]
                SiceAngle = EMPAngle2 + 2 * np.pi - EMPAngle
                HalfAngle = EMPAngle2 + SiceAngle/2
            if HalfAngle > 2 * np.pi:
                HalfAngle = HalfAngle - 2 * np.pi
                 
        EM3 = [SiceAngle,HalfAngle,EMPAngle,EMPAngle2]

        return [EM1, EM2,EM3]
    
    def  AngleHalfAndSice(self,Ang1,Ang2):   

        SiceAngle = abs(Ang1-Ang2) # AngleSice
        HalfAngle = (Ang1+Ang2)/2

        if SiceAngle > np.pi:
            SiceAngle = 2* np.pi - SiceAngle
            HalfAngle = HalfAngle - np.pi 


        return SiceAngle,HalfAngle


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

