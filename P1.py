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
                SSAnglesLM, SSAnglesEmpty= self.AnglestoLM(CP) #Snapshot to LM Current Point
                AngleLMMidx = self.MatchTPAngles(SSAnglesLM,TPAngleLM) #Matching Angles
                AngleEmtMidx = self.MatchTPAngles(SSAnglesEmpty,TPAngleEmpty) #Matching Angles
                DirectionVectorLm = self.FinalVectorCalc(SSAnglesLM,TPAngleLM,AngleLMMidx)
                DirectionVectorEmt = self.FinalVectorCalc(SSAnglesEmpty,TPAngleEmpty,AngleEmtMidx)
                FinaleVectorDirection = (DirectionVectorLm + DirectionVectorEmt)/2

    def FinalVectorCalc(self,AngSS,AngTP,AndiD): 
        UV = self.UnitVecCalc(AngTP[0][0],AngSS[AndiD[0]][0],AngSS[AndiD[0]][1])
        UV = UV + self.UnitVecCalc(AngTP[1][0],AngSS[AndiD[1]][0],AngSS[AndiD[1]][1])
        UV = UV +self.UnitVecCalc(AngTP[2][0],AngSS[AndiD[2]][0],AngSS[AndiD[2]][1])

        AV = self.AngVecCalc(AngTP[0][1],AngSS[AndiD[0]][1],AngTP[0][0])
        AV = AV + self.AngVecCalc(AngTP[1][1],AngSS[AndiD[1]][1],AngTP[1][0])
        AV = AV + self.AngVecCalc(AngTP[2][1],AngSS[AndiD[2]][1],AngTP[2][0])

        FinalAng = (UV + AV * 3)/4
        return FinalAng

    def AngVecCalc(self,AngSS,AngTP,AngTPS): 
        if AngSS == AngTP:
            Ang=0
        else:
            if AngTP - np.pi <0:
                if 2 * np.pi - ( AngTP - np.pi) < AngSS or AngSS < AngTP: #is negativ the right direction?
                    if AngTPS<=np.pi: # TP < 180
                        Ang = AngSS - np.pi/2
                    else:
                        Ang = AngSS + np.pi/2
                else:
                    if AngTPS>np.pi: # TP > 180
                        Ang = AngSS - np.pi/2
                    else:
                        Ang = AngSS + np.pi/2
            else:
                if  AngTP - np.pi > AngSS or AngSS > AngTP: #is negativ the right direction?
                    if AngTPS<=np.pi: # TP < 180
                        Ang = AngSS - np.pi/2
                    else:
                        Ang = AngSS + np.pi/2
                else:
                    if AngTPS>np.pi: # TP > 180
                        Ang = AngSS - np.pi/2
                    else:
                        Ang = AngSS + np.pi/2

        if Ang < 0:
            Ang = 2 * np.pi + Ang
        if Ang > 2 * np.pi:
            Ang= Ang - 2 * np.pi 

        return Ang

    def UnitVecCalc(self,AngSSSice,AngTPSice,AngSSD): 
        if AngSSSice > AngTPSice:
            Ang = AngSSD
        elif AngSSSice < AngTPSice:
            Ang = AngSSD + np.pi
            if Ang >=  np.pi * 2:
                Ang = Ang - 2* np.pi
        else:
            Ang = 0

        return Ang

    def MatchTPAngles(self,SSAngles,TPAngles): 
        SSAnglelist= [SSAngles[0][1],SSAngles[1][1],SSAngles[2][1]]
        idx = []
        for i in range(len(SSAngles)):
            SSAnglelist = np.asarray(SSAnglelist)
            cal = (np.abs(SSAnglelist - TPAngles[i][1])).argmin()
            calcmax = (np.abs(SSAnglelist - TPAngles[i][1])).argmax()
            if np.abs(SSAnglelist - TPAngles[calcmax][1])>= np.pi:
                if  np.abs(SSAnglelist - TPAngles[calcmax][1]) - np.pi < np.abs(SSAnglelist - TPAngles[calc][1]):
                    calc = calcmax
            idx.append[calc]  
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
        Ang1= Xline.smallest_angle_between(ln1) #Angle of 1 LMpoint to X
        ln2=Line(CP,INPoints[1])
        Ang2 = Xline.smallest_angle_between(ln2) #Angle of 2 LMpoint to X

        if  INPoints[0].args[1]<0: # if negativ Y angle negativ  
            if  INPoints[0].args[0]>0: # if positiv  X angle positiv
                Ang1 = 2 * np.pi - Ang1
            else:
                Ang1 = Ang1 + np.pi
        elif INPoints[0].args[0]<0: # if negativ  X angle negativ
            Ang1 = np.pi - Ang1

        if  INPoints[1].args[1]<0: # if negativ Y angle negativ  
            if  INPoints[1].args[0]>0: # if positiv  X angle positiv
                Ang2 = 2 * np.pi - Ang2
            else:
                Ang2 = Ang2 + np.pi
        elif INPoints[1].args[0]<0: # if negativ  X angle negativ
            Ang2 = np.pi - Ang2

        SiceAngle = abs(Ang1-Ang2) # AngleSice
        HalfAngle = (Ang1+Ang2)/2
        if SiceAngle > np.pi:
            SiceAngle = 2* np.pi - SiceAngle
            HalfAngle = HalfAngle - np.pi 
        return [SiceAngle,HalfAngle,Ang1,Ang2]

    def AngleEtCalc(self,CP,LM1,LM2,LM3): 
        LM = [LM1, LM2 , LM3]
        LM.sort(key=lambda HAng: HAng[1])

        EM1 = self.EmptyAngelCalc(0,1,LM)
        EM2 = self.EmptyAngelCalc(1,2,LM)            
        EM3 = self.EmptyAngelCalc(2,0,LM)
        return [EM1,EM2,EM3]
    
    def  EmptyAngelCalc(self,idx1,idx2,LM):   

        if (4.71<LM[idx1][2] or 4.71<LM[idx1][3]) and (LM[idx1][2]<1.57 or LM[idx1][3]<1.57):
            if LM[idx1][2]<LM[idx1][3]: #LM liegt auf X Achse
                EMPAngle=LM[idx1][2]
            else:
                EMPAngle=LM[idx1][3]
        else:    
            if LM[idx1][2]>LM[idx1][3]: #LM liegt nicht auf X Achse
                EMPAngle=LM[idx1][2]
            else:
                EMPAngle=LM[idx1][3]

        if (4.71<LM[idx2][2] or 4.71<LM[idx2][3]) and (LM[idx2][2]<1.57 or LM[idx2][3]<1.57):
            if LM[idx2][2]>LM[idx2][3]: #LM liegt auf X Achse
                EMPAngle2=LM[idx2][2]
            else:
                EMPAngle2=LM[idx2][3]
        else:
            if LM[idx2][2]<LM[idx2][3]: #LM liegt nicht auf X Achse
                EMPAngle2=LM[idx2][2]
            else:
                EMPAngle2=LM[idx2][3]
        if EMPAngle2>=EMPAngle:
            SiceAngle = EMPAngle2 - EMPAngle
            HalfAngle = (EMPAngle + EMPAngle2)/2
        else:
            SiceAngle = EMPAngle2 + 2 * np.pi - EMPAngle
            HalfAngle = EMPAngle + SiceAngle/2 
            if HalfAngle > 2 * np.pi:
                HalfAngle = HalfAngle - 2 * np.pi
        return [SiceAngle,HalfAngle,EMPAngle,EMPAngle2]


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

