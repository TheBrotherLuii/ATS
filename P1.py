import numpy as np
import matplotlib.pyplot as plt
import sys 

from sympy import Eq,pi,cos,sin
from sympy.geometry import Point, Circle, Line

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen

class StartScreen(Screen,GridLayout):

    def __init__(self,**kwargs):
        super(StartScreen,self).__init__(**kwargs)
        #Interface
        self.cols = 3

        #Start Screen discription
        self.add_widget(Label(text='',font_size='20sp'))
        self.add_widget(Label(text='X-Value',font_size='20sp'))
        self.add_widget(Label(text='Y-Value',font_size='20sp'))

        self.add_widget(Label(text='Landmark 1',font_size='20sp'))
        self.LM1_X = Spinner(text='X',values=("-7","-6","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7"),font_size='50sp')
        self.add_widget(self.LM1_X)
        self.LM1_Y = Spinner(text='Y',values=("-7","-6","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7"),font_size='50sp')
        self.add_widget(self.LM1_Y)

        self.add_widget(Label(text='Landmark 2',font_size='20sp'))
        self.LM2_X = Spinner(text='X',values=("-7","-6","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7"),font_size='50sp')
        self.add_widget(self.LM2_X)
        self.LM2_Y = Spinner(text='Y',values=("-7","-6","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7"),font_size='50sp')
        self.add_widget(self.LM2_Y)

        self.add_widget(Label(text='Landmark 3',font_size='20sp'))
        self.LM3_X = Spinner(text='X',values=("-7","-6","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7"),font_size='50sp')
        self.add_widget(self.LM3_X)
        self.LM3_Y = Spinner(text='Y',values=("-7","-6","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7"),font_size='50sp')
        self.add_widget(self.LM3_Y)

        self.add_widget(Label(text=''))
        DrawButton = Button(text='Draw' ,font_size='60sp',background_color=[0,1,0,1])
        DrawButton.bind(on_press = self.CalculateDrawing)
        self.add_widget(DrawButton)
        self.add_widget(Label(text=''))

    def changer(self,*args):
        self.manager.current = 'ErrorScreen'

    def areLandmarksSet(self):
        if (self.LM1_X.text or self.LM1_Y.text or self.LM2_X.text or self.LM2_Y.text or self.LM3_X.text or self.LM3_Y.text) == ('X' or 'Y'):
            return self.changer()


    def CalculateDrawing(self,instance):

        self.areLandmarksSet()

        #setting up LandMark Centers
        self.LM1P = Point(float(self.LM1_X.text),float(self.LM1_Y.text))
        self.LM2P = Point(float(self.LM2_X.text),float(self.LM2_Y.text))
        self.LM3P = Point(float(self.LM3_X.text),float(self.LM3_Y.text))
       
        TPP = Point(0,0)  #setting up TargetPoint Points
        TPAngleLM, TPAngleEmpty = self.AnglestoLM(TPP)#Angel to LM
        #setting up meshgris -7 to 7
        xx,yy  = np.meshgrid(np.arange(-7, 8, 1),np.arange(-7, 8, 1), indexing='xy')
        xz = [[0] * len(xx) for i in range(len(yy))]
        yz = [[0] * len(xx) for i in range(len(yy))]
        for i in range(len(xx)):
            for j in range(len(yy)):
                CP = Point(xx[j,i],yy[j,i]) #Current Loop Point
                SSAnglesLM, SSAnglesEmpty= self.AnglestoLM(CP) #Snapshot to LM Current Point
                AngleLMMidx = self.MatchTPAngles(SSAnglesLM,TPAngleLM) #Matching Angles
                AngleEmtMidx = self.MatchTPAngles(SSAnglesEmpty,TPAngleEmpty) #Matching Angles
                DirectionVectorLm = self.FinalVectorCalc(SSAnglesLM,TPAngleLM,AngleLMMidx)
                DirectionVectorEmt = self.FinalVectorCalc(SSAnglesEmpty,TPAngleEmpty,AngleEmtMidx)                
                FAngle = (DirectionVectorLm + DirectionVectorEmt)/2
                xz[j][i] = int((cos(FAngle) + xx[j,i])*-1000)
                yz[j][i] = int((sin(FAngle) + yy[j,i])*-1000)

        self.QuiverPlot(xz,yz)

    def FinalVectorCalc(self,AngSS,AngTP,AndiD): 
        UV = self.UnitVecCalc(AngTP[0][0],AngSS[AndiD[0]][0],AngSS[AndiD[0]][1])
        UV = UV + self.UnitVecCalc(AngTP[1][0],AngSS[AndiD[1]][0],AngSS[AndiD[1]][1])
        UV = UV +self.UnitVecCalc(AngTP[2][0],AngSS[AndiD[2]][0],AngSS[AndiD[2]][1])
        UV = UV /3
        AV = self.AngVecCalc(AngTP[0][1],AngSS[AndiD[0]][1],AngTP[0][0])
        AV = AV + self.AngVecCalc(AngTP[1][1],AngSS[AndiD[1]][1],AngTP[1][0])
        AV = AV + self.AngVecCalc(AngTP[2][1],AngSS[AndiD[2]][1],AngTP[2][0])
        AV = AV /3
        FinalAng = (UV+AV+AV+AV)/4
        return FinalAng

    def AngVecCalc(self,AngSS,AngTP,AngTPS): 
        if AngSS == AngTP:
            Ang=0
        else:
            if AngTP - np.pi <0:
                if 2 * np.pi - ( AngTP - np.pi) < AngSS or AngSS < AngTP: #is negativ the right direction?
                    if AngTPS<=np.pi: # TP < 180
                        Ang = AngSS - (np.pi)/2
                    else:
                        Ang = AngSS + (np.pi)/2
                else:
                    if AngTPS>np.pi: # TP > 180
                        Ang = AngSS - (np.pi)/2
                    else:
                        Ang = AngSS + (np.pi)/2
            else:
                if  AngTP - np.pi > AngSS or AngSS > AngTP: #is negativ the right direction?
                    if AngTPS<=np.pi: # TP < 180
                        Ang = AngSS - (np.pi)/2
                    else:
                        Ang = AngSS + (np.pi)/2
                else:
                    if AngTPS>np.pi: # TP > 180
                        Ang = AngSS - (np.pi)/2
                    else:
                        Ang = AngSS + (np.pi)/2

                if Ang>2 * np.pi:
                    Ang= Ang - 2 * np.pi 
                elif Ang<0:
                    Ang = 2 * np.pi + Ang
        
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
            calc = (np.abs(SSAnglelist - TPAngles[i][1])).argmin()
            calcmax = (np.abs(SSAnglelist - TPAngles[i][1])).argmax()
            if np.abs(SSAnglelist[calcmax] - TPAngles[i][1]) >= np.pi:
                if  np.abs(SSAnglelist[calcmax] - TPAngles[i][1]) - np.pi < np.abs(SSAnglelist[calc] - TPAngles[i][1]):
                    calc = calcmax
            idx.append(calc) 
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

        CP2 = CP + (1,0)
        Xline = Line (CP, CP2) #x-Line
        INPoints = self.InterPointCalc(CP,LMP) #Calculate outside Points of LM from CP
        if len(INPoints)==2:
            ln1=Line(CP,INPoints[0])
            Ang1= Xline.smallest_angle_between(ln1).evalf() #Angle of 1 LMpoint to X
            ln2=Line(CP,INPoints[1])
            Ang2 = Xline.smallest_angle_between(ln2).evalf() #Angle of 2 LMpoint to X
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
        else:
            Ang1 = 0
            Ang2 = 0
            SiceAngle = 0
            HalfAngle = 0

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
                if LM[idx2][2]>LM[idx2][3]: #LM liegt auf X Ahanghse
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

    def QuiverPlot(self,gridx,gridy):
        # Create quiver figure
        fig, ax = plt.subplots()
        ax.axis([-7, 7, -7, 7])

        x, y = np.meshgrid(np.arange(-7, 8, 1), np.arange(-7, 8, 1))
        
        ax.quiver(x,y,gridx,gridy,angles='uv', scale_units='xy', scale=4000,minshaft = 5, headwidth=5)

        LMX=np.array([float(self.LM1_X.text), float(self.LM2_X.text) ,float(self.LM3_X.text)])
        LMY=np.array([float(self.LM1_Y.text),float(self.LM2_Y.text),float(self.LM3_Y.text)])
        ax.scatter(0,0,color='r',s=200)  #Honeypot
        ax.scatter(LMX,LMY,color='g',s=150) #Landmarks

        ax.set_title('Honey Way')
        plt.show()

class ErrorScreen(Screen):

    def __init__ (self,**kwargs):
        super (ErrorScreen, self).__init__(**kwargs)

        self.add_widget(Label(text='Please set all Landmarks'))
        DrawButton = Button(text='ok' ,font_size='60sp',background_color=[1,0,0,0])
        DrawButton.bind(on_press = self.changer())
        self.add_widget(DrawButton)
        self.add_widget(Label(text=''))

    def changer(self):
        sm.current = 'Start'
        return True
 
class TestApp(App):
    def build(self):
        return sm

sm = ScreenManager()
sm.add_widget(StartScreen(name='Start'))
sm.add_widget(ErrorScreen(name='Error'))
TestApp().run()

