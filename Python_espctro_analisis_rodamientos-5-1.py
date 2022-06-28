from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image
#-----------------------------

from math import(trunc)
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec
import numpy as np
import scipy as scpD
from scipy.signal.windows import hann
from scipy.signal import find_peaks
from mpl_toolkits.mplot3d.axes3d import Axes3D

from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *

from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy.signal import butter, lfilter, freqz

from matplotlib.widgets import Cursor
from scipy.stats import norm, kurtosis
from scipy.stats import skew
#from scipy.signal import hilbert
from scipy.fftpack import hilbert


#print(plt.style.available)
#==============================================================================

# definir funciones

#=============================================================================
    
def SelectFichero():
    
    global Nombrefichero
    
    #Nombrefichero=""
    Nombrefichero = askopenfilename(title="Select a file to analysis", filetypes=(("UFF files","*.UFF"),("All files","*.*")))
    if Nombrefichero!="":
            label_Nombrefichero =Label(text="", bg="gray", fg="white", width=110)
            label_Nombrefichero =Label(text=Nombrefichero, bg="gray", fg="white", width=100)
            label_Nombrefichero.place(x=50, y=50)
    if Nombrefichero=="":
        label_Nombrefichero =Label(text="", bg="gray", fg="white", width=110)
            



    #--------------------------------------------------------------------------



                
    return

def SelectFicheroReferencia():
    
    global Nombrefichero_Ref
       
    Nombrefichero_Ref=""
    Nombrefichero_Ref = askopenfilename(title="Select a Baseline file", filetypes=(("UFF files","*.UFF"),("All files","*.*")))
    if Nombrefichero_Ref!="":
            
        label_Nombrefichero_Ref =Label(text="", bg="gray", fg="white", width=100)
        label_Nombrefichero_Ref =Label(text=Nombrefichero_Ref, bg="gray", fg="white", width=100)
        label_Nombrefichero_Ref.place(x=50, y=80)
    if Nombrefichero_Ref=="":
        label_Nombrefichero_Ref =Label(text="", bg="gray", fg="white", width=110)
   
    return




    #--------------------------------------------------------------------------



def Leer_FicheroUFF_Med():
           
        global Valores
        global kini
        global k_parametro
        global bool_LeerUFF_Fault
        global label_Nombrefichero
        #global Descrip_PMed
        #global Descrip_PMed2

        #Nombrefichero=""
        #Nombrefichero = askopenfilename(title="Select a file to analysis", filetypes=(("UFF files","*.UFF"),("All files","*.*")))
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        if Nombrefichero!="":
             
            showinfo(title='', message='Processing the measurement files'+Nombrefichero+ ' ... please wait') 
             
            Valores=[line.strip() for line in open(Nombrefichero)] 
            Cant_Valores=len(Valores)
            #print ("Lectura del espectro : ",Nombrefichero)
            #print("Cantidad de lineas leidas", Cant_Valores)
            
            #==============================================================
            
            # IMPORTANTE
            # Obtener campos de los parametros del primer espectro
            
            Nombre_PMed[0]="Wind turbogenerator code" 
            Nombre_PMed[1]="Measurement Point"
            Nombre_PMed[2]="Measurement date"
            Nombre_PMed[3]="Samples size (amount of samples)"
            Nombre_PMed[4]="Sample time"
            Nombre_PMed[5]="Sample frequency (calculate)"
            Nombre_PMed[6]="Sensibility"
            Nombre_PMed[7]="Unit"
            Nombre_PMed[8]="Measurement point description"
                
                       
            #print(" ")
            #print ("estos son los parametros seleccionados del primer espectro")
            #print(" ")
           
            #print(Nombre_PMed)
            
            # Introducir valores cuantitativos de los parametros
            #=====================================================
            
            # P_Med2[Punto_Med] implica parametros de medicion
            # Introducir descripcion de cada parametro (0 - 11)
                
            kini=2595
            
            for Punto_Med in range(0,11):
                   
                    # Wind turbogenerator code
                    try:
                        k_parametro=kini+5
                        P_Med2[Punto_Med][0]=Valores[k_parametro]
                    except:
                        P_Med2[Punto_Med][0]="48844-WTG01_Error"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Wind turbogenerator code- Format error in file -Default value 48844-WTG01_Error will be using ') 
                    
                    # Measurement point
                    try:
                        k_parametro=kini+6
                        A= Valores[k_parametro].split(",") [0]
                        B= A.split(";")[0]
                        P_Med2[Punto_Med][1]=B
                    except:
                        P_Med2[Punto_Med][1]="Point_Error"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Measurement point- Format error in file -Default value: Point_Error will be using ') 
                    
                    # Measurement date
                    try:
                        k_parametro=kini+4
                        P_Med2[Punto_Med][2]=Valores[k_parametro]
                        global fecha1
                        fecha1=P_Med2[Punto_Med][2]
                    except:
                        P_Med2[Punto_Med][2]="00-12-31T05:30:26Z"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Measurement date- Format error in file -Default value: 00-12-31T05:30:26Z will be using ')
                        
                    # Samples size (amount of samples)
                    try:
                        k_parametro=kini+8
                        A= Valores[k_parametro].split(" ") [4]
                        P_Med2[Punto_Med][3]=A
                    except:
                        P_Med2[Punto_Med][3]="262144"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Samples size (amount of samples)- Format error in file -Default value:262144 will be using ')
                        
                    # Sample time
                    try:
                        k_parametro=kini+9
                        A= Valores[k_parametro].split(" ") [0]
                        P_Med2[Punto_Med][4]=A
                    except:
                        P_Med2[Punto_Med][4]="17"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Sample time- Format error in file -Default value: 17 will be using ')
                        
                    # Sample frequency (calculate)
                    try:
                        k_parametro=kini+8
                        A= Valores[k_parametro].split(" ") [17]
                        B=float(A)
                        B=1/B
                        C=str(B)
                        P_Med2[Punto_Med][5]=C
                    except:
                        P_Med2[Punto_Med][5]="25600.0"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Sample frequency (calculate)- Format error in file -Default value:25600.0 will be using ')
                    
                    # Sensibility
                    try:
                        P_Med2[Punto_Med][6]="1"
                        if Punto_Med!=2 :
                            k_parametro=kini+6
                            A= Valores[k_parametro].split(",") [1]
                            B= A.split(";")[0]
                            P_Med2[Punto_Med][6]=B
                            
                            #A1 =float(P_Med2[Punto_Med][6])
                            #print(A1)
                            #print("sensibilidad",P_Med2[Punto_Med][6])
                    except:
                        P_Med2[Punto_Med][6]="0102"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Sensibility - Format error in file -Default value: 0102 will be using ')
                    
                    # Unit
                    try:
                        P_Med2[Punto_Med][7]="V"
                        if Punto_Med!=2 :
                            k_parametro=kini+6
                            Valores[k_parametro].split(",") [1]
                            B= A.split(";")[1]   
                            P_Med2[Punto_Med][7]=B
                    except:
                        P_Med2[Punto_Med][7]="m/s2"
                        showinfo(title='Warning', message=Descrip_PMed[Punto_Med]+": "+'Unit- Format error in file -Default value: m/s2 will be using ')
                        
                    # Measurement point description
                    k_parametro=kini+10
                    P_Med2[Punto_Med][8]=Descrip_PMed[Punto_Med]
                            
                    #print("Med No",Punto_Med,":",P_Med2[Punto_Med][N1+0],P_Med2[Punto_Med][N1+1],P_Med2[Punto_Med][N1+2],P_Med2[Punto_Med][N1+3],P_Med2[Punto_Med][N1+4],P_Med2[Punto_Med][N1+5],P_Med2[Punto_Med][N1+6],P_Med2[Punto_Med][N1+7],P_Med2[Punto_Med][N1+8])
                    #print(P_Med2[Punto_Med]) # lista de algunos parametros de medicion almacenada en el UFF
                    
                    kini+=65550
                    
            # Definir posicion de separadores en el fichero UFF
            # inicio de med. para cada parametro a partir de la linea 2595
            #=============================================================
        
            Pos_SeparadorUFF=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            N1=2595
            M=0
            for i in range(0,12):
                # 12 => Generar el limite superior del parametro 11
                Pos_SeparadorUFF[i]=N1+i*65550
                #print(i, Pos_SeparadorUFF[i], Valores[Pos_SeparadorUFF[i-1]])
                M=M+1
             
                
            # Introducir valores cuantitativos de la senal en el tiempo de cada parametro 
            #============================================================================
                
            
            # Visualizar los separadores existentes en el fcihero UFF
            
            #try:
            e=0
            if e==0:                    
                kini=2595
                bool_LeerUFF_Fault=FALSE
                
                for Punto_Med in range(0,11):
                    #N1 y N2 son el numero de la linea en el fichero UFF
                    N1=Pos_SeparadorUFF[Punto_Med]+13
                    N2=Pos_SeparadorUFF[Punto_Med+1]-2
                    #print("Punto_Med, N1,N2",Punto_Med, N1,N2)
                    
                    Sensibilidad=float(P_Med2[Punto_Med][6])
                    M=0
                    for i in range(N1,N2):
                        M_Med2[Punto_Med][M+0]=float(Valores[i].split()[0])/Sensibilidad
                        M_Med2[Punto_Med][M+1]=float(Valores[i].split()[1])/Sensibilidad
                        M_Med2[Punto_Med][M+2]=float(Valores[i].split()[2])/Sensibilidad
                        M_Med2[Punto_Med][M+3]=float(Valores[i].split()[3])/Sensibilidad
                        M=M+4
                
                for Punto_Med in range(0,11):
                    N2=Pos_SeparadorUFF[Punto_Med+1]-2     
                    N1=Pos_SeparadorUFF[Punto_Med]+13

                    #print (M,Descrip_PMed[Punto_Med],N1, N2,N2-20,  N2-N1)
                    #U=Pos_SeparadorUFF[Punto_Med]
                    #print(M_Med2[Punto_Med][U])

                    Last=0.0001
                    for i in range(0, 262144):
                        if M_Med2[Punto_Med][i]>0:
                            Last=M_Med2[Punto_Med][i]
                        if M_Med2[Punto_Med][i]<=0:
                            M_Med2[Punto_Med][i]=Last
                        
                    #for i in range(262124, 262144):        
                        #print(Punto_Med,i-262124, M_Med2[Punto_Med][i])
                        
                 
            #except:
                #showinfo(title='Warning', message=' Read of measurement error, UFF file :'+Nombrefichero )
                #bool_LeerUFF_Fault=TRUE
                 
    
            #print(kini,M_Med2[Punto_Med])
            # print(Punto_Med,Descrip_PMed[Punto_Med],kini,M_Med[kini])    

                                   
            #print("Terminado") 
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        else:
                      
            showarning(title='Warning', message='File not selected')    
        
            
        return
    




    #--------------------------------------------------------------------------




def Leer_FicheroUFF_Ref():
           
        global kini
        global k_parametro
        global bool_LeerUFF_Fault
        global label_Nombrefichero_Ref
        global Valores_Ref
         
        #global Descrip_PMed
        #global Descrip_PMed2

        #Nombrefichero=""
        #Nombrefichero = askopenfilename(title="Select a file to analysis", filetypes=(("UFF files","*.UFF"),("All files","*.*")))
        #print ("Nombre fichero REF",Nombrefichero_Ref)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                
        if Nombrefichero_Ref!="":
            
             
            showinfo(title='', message='Processing the Baseline files '+Nombrefichero_Ref+' ... please wait') 
             
            Valores_Ref=[line.strip() for line in open(Nombrefichero_Ref)] 
            Cant_Valores=len(Valores_Ref)
            
            #print ("Lectura del espectro : ",Nombrefichero_Ref)
            #print("Cantidad de lineas leidas", Cant_Valores)
            #print("Valores_Ref",Valores_Ref[44])
            
            
            #==============================================================
            
            # IMPORTANTE
            # Obtener campos de los parametros del primer espectro
            
            Nombre_PRef[0]="Wind turbogenerator code" 
            Nombre_PRef[1]="Measurement Point"
            Nombre_PRef[2]="Measurement date"
            Nombre_PRef[3]="Samples size (amount of samples)"
            Nombre_PRef[4]="Sample time"
            Nombre_PRef[5]="Sample frequency (calculate)"
            Nombre_PRef[6]="Sensibility"
            Nombre_PRef[7]="Unit"
            Nombre_PRef[8]="Measurement point description"
                
                       
            #print(" ")
            #print ("estos son los parametros seleccionados del primer espectro")
            #print(" ")
           
            #print(Nombre_PRef)
            
            # Introducir valores cuantitativos de los parametros
            #=====================================================
            
            # P_Ref2[Punto_Ref] implica parametros de medicion
            # Introducir descripcion de cada parametro (0 - 11)
                
            kini=2595
            
            for Punto_Ref in range(0,11):
                   
                    # Wind turbogenerator code
                    try:
                        k_parametro=kini+5
                        P_Ref2[Punto_Ref][0]=Valores_Ref[k_parametro]
                    except:
                        P_Ref2[Punto_Ref][0]="48844-WTG01_Error"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Wind turbogenerator code- Format error in file -Default value 48844-WTG01_Error will be using ') 
                    
                    # Measurement point
                    try:
                        k_parametro=kini+6
                        A= Valores_Ref[k_parametro].split(",") [0]
                        B= A.split(";")[0]
                        P_Ref2[Punto_Ref][1]=B
                    except:
                        P_Ref2[Punto_Ref][1]="Point_Error"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Measurement point- Format error in file -Default value: Point_Error will be using ') 
                    
                    # Measurement date
                    try:
                        k_parametro=kini+4
                        P_Ref2[Punto_Ref][2]=Valores_Ref[k_parametro]
                        global fecha2
                        fecha2=P_Ref2[Punto_Ref][2]
                    except:
                        P_Ref2[Punto_Ref][2]="00-12-31T05:30:26Z"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Measurement date- Format error in file -Default value: 00-12-31T05:30:26Z will be using ')
                        
                    # Samples size (amount of samples)
                    try:
                        k_parametro=kini+8
                        A= Valores_Ref[k_parametro].split(" ") [4]
                        P_Ref2[Punto_Ref][3]=A
                    except:
                        P_Ref2[Punto_Ref][3]="262144"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Samples size (amount of samples)- Format error in file -Default value:262144 will be using ')
                        
                    # Sample time
                    try:
                        k_parametro=kini+9
                        A= Valores_Ref[k_parametro].split(" ") [0]
                        P_Ref2[Punto_Ref][4]=A
                    except:
                        P_Ref2[Punto_Ref][4]="17"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Sample time- Format error in file -Default value: 17 will be using ')
                        
                    # Sample frequency (calculate)
                    try:
                        k_parametro=kini+8
                        A= Valores_Ref[k_parametro].split(" ") [17]
                        B=float(A)
                        B=1/B
                        C=str(B)
                        P_Ref2[Punto_Ref][5]=C
                    except:
                        P_Ref2[Punto_Ref][5]="25600.0"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Sample frequency (calculate)- Format error in file -Default value:25600.0 will be using ')
                    
                    # Sensibility
                    try:
                        P_Ref2[Punto_Ref][6]="1"
                        if Punto_Ref!=2 :
                            k_parametro=kini+6
                            A= Valores_Ref[k_parametro].split(",") [1]
                            B= A.split(";")[0]
                            P_Ref2[Punto_Ref][6]=B
                            
                            #A1 =float(P_Ref2[Punto_Ref][6])
                            #print(A1)
                            #print("sensibilidad",P_Ref2[Punto_Ref][6])
                    except:
                        P_Ref2[Punto_Ref][6]="0102"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Sensibility - Format error in file -Default value: 0102 will be using ')
                    
                    # Unit
                    try:
                        P_Ref2[Punto_Ref][7]="V"
                        if Punto_Ref!=2 :
                            k_parametro=kini+6
                            Valores_Ref[k_parametro].split(",") [1]
                            B= A.split(";")[1]   
                            P_Ref2[Punto_Ref][7]=B
                    except:
                        P_Ref2[Punto_Ref][7]="m/s2"
                        showinfo(title='Warning', message=Descrip_PRef[Punto_Ref]+": "+'Unit- Format error in file -Default value: m/s2 will be using ')
                        
                    # Measurement point description
                    k_parametro=kini+10
                    P_Ref2[Punto_Ref][8]=Descrip_PRef[Punto_Ref]
                            
                    #print("Ref No",Punto_Ref,":",P_Ref2[Punto_Ref][N1+0],P_Ref2[Punto_Ref][N1+1],P_Ref2[Punto_Ref][N1+2],P_Ref2[Punto_Ref][N1+3],P_Ref2[Punto_Ref][N1+4],P_Ref2[Punto_Ref][N1+5],P_Ref2[Punto_Ref][N1+6],P_Ref2[Punto_Ref][N1+7],P_Ref2[Punto_Ref][N1+8])
                    #print(P_Ref2[Punto_Ref]) # lista de algunos parametros de Reficion almacenada en el UFF
                    
                    kini+=65550
                    
            # Definir posicion de separadores en el fichero UFF
            # inicio de Ref. para cada parametro a partir de la linea 2595
            #=============================================================
        
            Pos_SeparadorUFF=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            N1=2595
            M=0
            for i in range(0,12):
                # 12 => Generar el limite superior del parametro 11
                Pos_SeparadorUFF[i]=N1+i*65550
                #print(i, Pos_SeparadorUFF[i], Valores[Pos_SeparadorUFF[i-1]])
                M=M+1
             
                
            # Introducir valores cuantitativos de la senal en el tiempo de cada parametro 
            #============================================================================
                
            
            # Visualizar los separadores existentes en el fcihero UFF
            
            #try:
            e=0
            if e==0:                    
                kini=2595
                bool_LeerUFF_Fault=FALSE
                
                for Punto_Ref in range(0,11):
                    #N1 y N2 son el numero de la linea en el fichero UFF
                    N1=Pos_SeparadorUFF[Punto_Ref]+13
                    N2=Pos_SeparadorUFF[Punto_Ref+1]-2
                    #print("Punto_Ref, N1,N2",Punto_Ref, N1,N2)
                    
                    Sensibilidad=float(P_Ref2[Punto_Ref][6])
                    M=0
                    for i in range(N1,N2):
                        M_Ref2[Punto_Ref][M+0]=float(Valores_Ref[i].split()[0])/Sensibilidad
                        M_Ref2[Punto_Ref][M+1]=float(Valores_Ref[i].split()[1])/Sensibilidad
                        M_Ref2[Punto_Ref][M+2]=float(Valores_Ref[i].split()[2])/Sensibilidad
                        M_Ref2[Punto_Ref][M+3]=float(Valores_Ref[i].split()[3])/Sensibilidad
                        M=M+4
                
                for Punto_Ref in range(0,11):
                    N2=Pos_SeparadorUFF[Punto_Ref+1]-2     
                    N1=Pos_SeparadorUFF[Punto_Ref]+13

                    #print (M,Descrip_PRef[Punto_Ref],N1, N2,N2-20,  N2-N1)
                    #U=Pos_SeparadorUFF[Punto_Ref]
                    #print(M_Ref2[Punto_Ref][U])

                    Last=0.0001
                    for i in range(0, 262144):
                        if M_Ref2[Punto_Ref][i]>0:
                            Last=M_Ref2[Punto_Ref][i]
                        if M_Ref2[Punto_Ref][i]<=0:
                            M_Ref2[Punto_Ref][i]=Last
                        
                    #for i in range(262124, 262144):        
                        #print(Punto_Ref,i-262124, M_Ref2[Punto_Ref][i])
                        
                 
            #except:
                #showinfo(title='Warning', message=' Read of measurement error, UFF file :'+Nombrefichero )
                #bool_LeerUFF_Fault=TRUE
                 
    
            #print(kini,M_Ref2[Punto_Ref])
            # print(Punto_Ref,Descrip_PRef[Punto_Ref],kini,M_Ref[kini])    

                                   
            #print("Terminado") 
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        else:
                      
            showinfo(title='Warning', message='File not selected')    
        
        # Valores_Ref FINALIZAR
        
        return




    #--------------------------------------------------------------------------




def CrearListas():
    
    # Inicializar Listas para guardar parametros y Reficioes
    
    global P_Med2
    global P_Ref2
    global M_Med2
    global M_Ref2
    global Pos_SeparadorUFF
    global Nombre_PMed
    global Nombre_PRef
    
    global Yt_Med
    global Yt_Ref
    global Yf_Ref
    
    
    global Nombre_PT
    global Nombre_PT2
    global Fila_PT
    global ValorPT_Med
    global ValorPT_Ref
       
    global Fila_NT
    global ValorNT_Med
    global ValorNT_Ref
    global Nombre_NT
    
    global Y_NT_ISO_ZonaBC
    global Y_NT_ISO_ZonaCD
    global X_NT_ISO
    global Y_NT_ComparativoBC
    global Y_NT_ComparativoCD
    
    
    """ No existen variables con subindices, se utilizan listas
    
    listas para guardar parametros y mediciones
    
    L_UM guarda los valores de amplitud de una senal en el tiempo
    Lista_Med guarda hasta 15 mediciones asociadas a cada uno de los puntos de medici'on'

    """
    
    #Prueba lista doble
    
    R=[0,0,0,0,0,0,0,0,0,0]
    H=[R,R,R,R,R,R,R,R,R,R]
    
    H[4][5]=25
    A=H[4][5]
    #print (A)
    
    
    
    #Creacion de las listas
    #=======================
    
    # Lista para parametros de la medicion  y de referencia 'VARIANTE LISTA DOBLE P_Med2[Punto_Med]2
    # Todos los valores se guardan como string
    
    # Puede almacenar informacion de hasta 15 puntos de medicion
    P_Med2= [ ["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""] ,["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""] ,["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""] , ["","","","","","","","","","","","","","",""] ] 
    # Puede almacenar informacion de hasta 15 puntos de medicion
    P_Ref2= [ ["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""] ,["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""] ,["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","",""] , ["","","","","","","","","","","","","","",""] ] 
    Nombre_PMed=["","","","","","","","","","","","","","",""]
    Nombre_PRef=["","","","","","","","","","","","","","",""]
    
    Nombre_PT=["Active power (MW)","Wind speed (m/s)","Ambient temperature  (°C)","Nacelle internal temperature  (°C)","Generator drive end bearing temperature  (°C)","Generator Non drive end bearing temperature  (°C)","Generator actual speed (Hz)","","","","",""]    # Nombre de los parametros funcionales
    Nombre_PT2=["PwAct (MW)","WdSpdAct (m/s)","AmbTmp (°C)","NacIntTmp (°C)","GnDeBrgTmp (°C)","GnNDeBrgTmp (°C)","GnSpdAct (Hz)","","","","",""]    # Codigo de los parametros funcionales
    Fila_PT=[43,133,148,163,208,193,463]  # Ubicacion de la fila que contiene el valor del parametro
    ValorPT_Med=[0,0,0,0,0,0,0]
    ValorPT_Ref=[0,0,0,0,0,0,0]
    
    
    Nombre_NT=["GnDe [10-5k]","GnNDe [10-5k]","Gx1Ps [0.1-10]","Gx1Ps [10-2k]","Gx2Ps [0.1-10]","Gx2Ps [10-2k]","GbxIssFr[0.1-10]","GbxIssFr [10-2k]","GbxIssRr [0.1-10]","GbxIssRr [10-2k]","GbxHssFr [0.1-10]","GbxHssFr [10-2k]","GbxHssRr [0.1-10]","GbxHssRr [10-2k]","NacZdir [0.1-10]","NacXdir [0.1-10]"]     # Ubicacion de la fila que contiene el valor del parametro
    
    Fila_NT=[748,988,1243,1258,1543,1558,1783,1798,2023,2038,2233,2248,2443,2458,2518,2593]    # Ubicacion de la fila que contiene el valor del parametro
    ValorNT_Med=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ValorNT_Ref=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
 
    X_NT_ISO=[0.5,1.5,1.5,2.5,2.5,3.5,3.5,4.5,4.5,5.5,5.5,6.5,6.5,7.5,7.5,8.5,8.5,9.5,9.5,10.5,10.5,11.5,11.5,12.5,12.5,13.5,13.5,14.5,14.5,15.5,15.5,16.5]
    Y_NT_ISO_ZonaCD=[16,16,16,16,0.5,0.5,12,12,0.5,0.5,12,12,0.5,0.5,12,12,0.5,0.5,12,12,0.5,0.5,12,12,0.5,0.5,12,12,0.5,0.5,0.5,0.5]
    Y_NT_ISO_ZonaBC=[10,10,10,10,0.3,0.3,7.5,7.5,0.3,0.3,7.5,7.5,0.3,0.3,7.5,7.5,0.3,0.3,7.5,7.5,0.3,0.3,7.5,7.5,0.3,0.3,7.5,7.5,0.3,0.3,0.3,0.3]
    
    Y=Y_NT_ComparativoBC= [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]
    Y=Y_NT_ComparativoCD= [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4] 
    
    
    
    #print (len(Y_NT_ISO_ZonaCD), len(X_NT_ISO))
    
    
    #print ("Longitud listas  NT",len(Fila_NT),len(ValorNT_Med),len(ValorNT_Ref), len (Nombre_NT))
    
    
    # En el registro P_Med2[Punto_Med]2[0][0] , [0][0], [0][0], ... [0][0] Se guardan los descriptores de parametros
    # Los valores se guardan cuando se acceda a Leerfichero
    
    #Lista para guardar mediciones M_Med2
    
    # realmente sobran 13 lineas en los registros de cada parametro 
    
    # Listas utilizadas para calcular y graficar FFT de la medicion y la referencia
    
    Yt_Med = np.zeros(262144) # SENAL A PROCESAR : senal en el tiempo del paramtro vigente a procesar
    Yt_Ref = np.zeros(262144) # SENAL DE REFERENCIA
    
    Yf_Ref=np.zeros(262144)

    # Procesa mediciones de 15 parametros
    M_Med2 = np.zeros((15,262144)) 
    # Procesa mediciones de 15 parametros
    M_Ref2 = np.zeros((15,262144)) 
        
    Pos_SeparadorUFF=np.zeros(15)
    
    # No se puede acceder a la lista Valores porque se crea dentro de Leerfichero
    # y esto sucede despues de leer el fichero seleccionado
    
    return  

      



    #--------------------------------------------------------------------------




def RadioButton_clicked(value):
    
    global Punto_Med_Select
    mylabel=Label(root, text=value)
    mylabel.place(x=300,y=150)
   
    Punto_Med_Select=value
    Graficar_EspectroTimeSignal()
    
    
    return





    #--------------------------------------------------------------------------




def Method_Changed(event):
    
    global method_selected    
   
    Method_Option=Combobox_Method.get()
       
    method_selected=2     
    
    if Method_Option=='Overall values':
             method_selected=0

    if Method_Option=='Time waveform signal analysis':
             method_selected=1
             
    if Method_Option== 'Frequency analysis':
             method_selected=2
             
    if Method_Option=='Dual analysis (times waveform - frequency)':
             method_selected=3
             
    if Method_Option=='Measurement / Baseline overall analysis':
             method_selected=4
             
    if Method_Option=='Comparative frequency analysis':
             method_selected=5
             
    if Method_Option=='Measurement / Baseline frequency analysis':
             method_selected=6
             
    if Method_Option=='Descriptors':
             method_selected=7
             
    if Method_Option=='Dual analysis (Measurement and baseline spectrum)':
             method_selected=8

    if Method_Option=='Comparative descriptors analysis':
             method_selected=9
   
    if Method_Option=='Waterfall':
             method_selected=10
             
    if Method_Option=='specturn density frecuency':
             method_selected=11
                     
    if Method_Option=='phase':
             method_selected=12
                     
    
    
    #print (method_selected) 
    
    return




    #--------------------------------------------------------------------------




def PointMed_Changed(event):
    
    global pointmed_selected
    
    PointMed_Option=Combobox_PuntoMed.get()
    
    pointmed_selected=0     
    
    if PointMed_Option== "1- Generator Drive End  m/s2":
             pointmed_selected=0
             
    if PointMed_Option== "2- Generator Non Drive End m/s2":
             pointmed_selected=1
             
    if PointMed_Option== "3- High Speed Shaft     V":
             pointmed_selected=2
             
    if PointMed_Option=="4- 1st Planetary Stage  m/s2":
             pointmed_selected=3
             
    if PointMed_Option=="5- 2nd Planetary Stage  m/s2":
             pointmed_selected=4

    if PointMed_Option=="6- Intermediate Speed Stage F m/s2":
             pointmed_selected=5

    if PointMed_Option=="7- Intermediate Speed Stage R m/s2":
             pointmed_selected=6

    if PointMed_Option=="8- High Speed Stage Fro m/s2":
             pointmed_selected=7

        
    if PointMed_Option=="9- High Speed Stage Rea m/s2":
             pointmed_selected=8

    if PointMed_Option=="10- Nacelle Z Direction  m/s2":
             pointmed_selected=9

    if PointMed_Option=="11- Nacelle X Direction  m/s2":
             pointmed_selected=10

    #print (pointmed_selected)   
    
    return





    #--------------------------------------------------------------------------




def Graficar_EspectroTimeSignal():
    
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    
    
    #Graficar time signal
    #----------------------
     
    #plt.figure(facecolor="black")   
    fig,ax = plt.subplots(1,2, figsize=[10,6])
    ax[0].plot(Xt, Yt_Med, color='skyblue') 
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
   
    ax[0].set_title(" Time waveform")
    ax[0].set_xlabel("Time in second (s)")
    ax[0].set_ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    
    #ax[0].fig(figsize=9,6)
    
    ax[0].grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
      
    # graficar espectros
    #---------------------
    
    w=hann(N)   #Ventana hanning
    
    Yf= rfft(Yt_Med)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    
    
    for i in range(0,20):
       Yf[i]=Yf[20]
   
    ax[1].plot(Xf, np.abs(Yf/Normalizado),color='skyblue')
    
    
    #Atributos
    #----------
    
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    ax[1].set_title(" Spectrum")
    ax[1].set_xlabel("Frequency (Hertz, Hz)")
    #ax[1].set_ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    ax[1].grid()
 
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[1], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
  
    # Graficar de forma simultanea Time wavw form y Spectrum
    
    plt.suptitle(" WTG : "+P_Med2[Punto_Med_Select][0] +Descrip_PMed2[Punto_Med_Select]+ ": Point No"+Descrip_PMed[Punto_Med_Select]+" Date: " + P_Med2[Punto_Med_Select][2])
    plt.show()
    
   
    return


    #--------------------------------------------------------------------------




def Graficar_EspectroMeasurementBaseline():
    
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    Yt_Ref=M_Ref2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    
        
    fig,ax = plt.subplots(1,2, figsize=[10,6])
    ax[0].plot(Xt, Yt_Med, color='skyblue') 
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
      
      
    # graficar espectros
    #---------------------
    
    w=hann(N)   #Ventana hanning
    
    Yf= rfft(Yt_Med)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    
    
    for i in range(0,20):
       Yf[i]=Yf[20]
   
    ax[0].plot(Xf, np.abs(Yf/Normalizado),color='skyblue')
    y1=np.abs(Yf/Normalizado)
  
    #Atributos
    #----------
    
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    ax[0].set_title(" Measurement spectrum")
    ax[0].set_xlabel("Frequency (Hertz, Hz)")
    #ax[0]].set_ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    ax[0].grid()
 
    Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[1], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    
    # graficar baseline espectro
    #---------------------
    
    w=hann(N)   #Ventana hanning
    
    Yf= rfft(Yt_Ref)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    
    
    for i in range(0,20):
       Yf[i]=Yf[20]
   
    ax[1].plot(Xf, np.abs(Yf/Normalizado),color='lime')
    y2= np.abs(Yf/Normalizado)
    
    #Atributos
    #----------
    
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    ax[1].set_title(" Baseline spectrum")
    ax[1].set_xlabel("Frequency (Hertz, Hz)")
    #ax[1].set_ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    ax[1].grid()
 
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[1], horizOn=True, vertOn=True, color='green', linewidth=2.0)
    
  
    
  
    # Graficar de forma simultanea Time wavw form y Spectrum
    
    plt.suptitle(" WTG : "+P_Med2[Punto_Med_Select][0] + Descrip_PMed2[Punto_Med_Select]+ ": Point No"+Descrip_PMed[Punto_Med_Select]+" Date: " + P_Med2[Punto_Med_Select][2])
    plt.show()
    
    
    espectro_cascada(Xf, y1, y2)
    espectro_cascada2()
   
    return

 

    #--------------------------------------------------------------------------




def Graficar_TimeSignal():
    
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    global Xt
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    
    
    #Graficar time signal
    #----------------------
     
    #plt.figure(facecolor="black")   
    fig = plt.figure(figsize=[10,6])
    plt.plot(Xt, Yt_Med, color='skyblue') 
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
   
    plt.title(" Time waveform:"+ Descrip_PMed2[Punto_Med_Select])
    plt.xlabel("Time in second (s)")
    plt.ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle(" WTG : "+P_Med2[Punto_Med_Select][0] +Descrip_PMed2[Punto_Med_Select]+ ": Point No"+Descrip_PMed[Punto_Med_Select]+" Date: " + P_Med2[Punto_Med_Select][2])
    
    evaluacion=evaluacion_rodamiento(Yt_Med)
    evolvente(Yt_Med,Xt,N,dt)
    plt.annotate(evaluacion,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(200, -330), textcoords='offset pixels',
                horizontalalignment='left',
                verticalalignment='top')
    plt.show()
    
   

    return

  


    #--------------------------------------------------------------------------




def Graficar_Spectrum():
    
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    
    
    
    # graficar espectros
    #---------------------
    
    w=hann(N)   #Ventana hanning
    
    Yf= rfft(Yt_Med)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    
    
    for i in range(0,20):
       Yf[i]=Yf[20]
    
    #plt.figure(facecolor="black")   
    fig = plt.figure(figsize=[10,6])
    plt.plot(Xf, np.abs(Yf/Normalizado),color='skyblue')
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
   
    plt.title(" Spectrum")
    plt.xlabel("Frequency in Hertz (Hz)")
    plt.ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle(" WTG : "+P_Med2[Punto_Med_Select][0] +Descrip_PMed2[Punto_Med_Select]+ ": Point No"+Descrip_PMed[Punto_Med_Select]+" Date: " + P_Med2[Punto_Med_Select][2])
    plt.show() 
    
   
    return




    #--------------------------------------------------------------------------



def Graficar_Spectrum_MedRef():
     
    showinfo(title=' ', message='MASK spectrum calculation (about 100 000 000 operation) ... please wait')   
    
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    Yt_Ref=M_Ref2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    
    # graficar espectro Medicion
    #---------------------------
    
    w=hann(N)   #Ventana hanning
    
    Yf= rfft(Yt_Med)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    
       
    
    #Para eliminar el valor de directa i=0
    #se igualan los primeros 20  valores => menor a 
    # 1Hz al valor 20th
    
    for i in range(0,20):
       Yf[i]=Yf[20]
    
    #plt.figure(facecolor="black")   
    fig = plt.figure(figsize=[10,6])
        
    #Graficar espectro referencia
    #----------------------------
    
    Yf_Ref= rfft(Yt_Ref)[0:N]
    Normalizado=N**0.5
    
    
    #Para eliminar el valor de directa i=0
    #se igualan los primeros 20  valores => menor a 
    # 1Hz al valor 20th
    
    for i in range(0,20):
       Yf_Ref[i]=Yf_Ref[20]
    
    #plt.figure(facecolor="black")   
   
    #print("grafico de la referencia")
    
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
   
    plt.title(" WTG : "+P_Med2[Punto_Med_Select][0] +" Measurement date: " + P_Med2[Punto_Med_Select][2]+ "Baseline date:" + P_Ref2[Punto_Med_Select][2])
    plt.xlabel("Frequency in Hertz (Hz)")
    plt.ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle(Descrip_PMed2[Punto_Med_Select]+ ": Point No"+Descrip_PMed[Punto_Med_Select])
   
    # correccion en frecuencia de la diferencia de rpm
    # entre medicion de referencia y la medicion
    
    A=ValorPT_Med[6]/ValorPT_Ref[6]
    
    MASK(Yf_Ref,800,1.3)
    
    plt.plot(Xf, np.abs(Yf/Normalizado), color='skyblue',label="Measure spectrum")
    plt.plot(Xf, Yf_MASK, color='blue', label= 'Baseline spectrum') 
    plt.legend()
    plt.show()  
    
  
    return





    #--------------------------------------------------------------------------



   

def MASK(Y,k, k_Esc):
    
    global Yf_MASK

    N=len(Y)
    Normalizado=N**0.5
    Yf_MASK=np.zeros(N)
    Y=np.abs(Y/Normalizado)
    
    for i in range(k+1,N-k):
        Mierda=0
        MaxVal=0
        
        #print (i,Mierda, MaxVal)
        
        for j in range(i-k,i+k):
            if Y[j]> MaxVal:
                MaxVal=Y[j]
            Mierda=j
            B=0
        Yf_MASK[i]=MaxVal    
        if k_Esc*MaxVal< 16:
            Yf_MASK[i]=k_Esc*MaxVal    
            
    for j in range (N-k, N-1):
        Yf_MASK[i]=Y[i]
        
        #print (i,Mierda, MaxVal,Yf_MASK[i],Y[j])
        #if i>7900:
            #print (i,Mierda,MaxVal,i-k, i+k, Y[i+k-1],Yf_MASK[i])
  
    
    return
    




    #--------------------------------------------------------------------------




def Graficar_Spectrum_MedEntreRef():
    
    
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    Yt_Ref=M_Ref2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    
    # graficar espectro Medicion
    #---------------------------
    
    w=hann(N)   #Ventana hanning
     
      
       
    Yf= rfft(Yt_Med)[0:N]
    Yf_Ref= rfft(Yt_Ref)[0:N]
    Xf= rfftfreq(N, dt)   
    Normalizado=N**0.5
    Diag_Val=Yf/Yf_Ref
       
    
    #Para eliminar el valor de directa i=0
    #se igualan los primeros 20  valores => menor a 
    # 1Hz al valor 20th
    
    for i in range(0,20):
       Diag_Val[i]=Diag_Val[20]
    
    #plt.figure(facecolor="black")   
    fig = plt.figure()
        
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
   
    plt.title(" WTG : "+P_Med2[Punto_Med_Select][0] +" Measurement date: " + P_Med2[Punto_Med_Select][2]+ "Baseline date:" + P_Ref2[Punto_Med_Select][2])
    plt.xlabel("Frequency in Hertz (Hz)")
    plt.ylabel("Dimensionless")
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle(Descrip_PMed2[Punto_Med_Select]+ ": Point No"+Descrip_PMed[Punto_Med_Select])
   
    # correccion en frecuencia de la diferencia de rpm
    # entre medicion de referencia y la medicion
    
       
    plt.plot(Xf, Diag_Val, color='green',label="Measure spectrum")
    plt.legend()
    plt.show()
    
    
    
    return






    #--------------------------------------------------------------------------







def Graficar_NT_Version2():
    
     
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    X=[0]
    Y=[0]
    Xt=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    
    # Nombre_NT=["GnDe [10-5k]","GnNDe [10-5k]","Gx1Ps [0.1-10]","Gx1Ps [10-2k]","Gx2Ps [0.1-10]","Gx2Ps [10-2k]","GbxIssFr[0.1-10]","GbxIssFr [10-2k]","GbxIssRr [0.1-10]","GbxIssRr [10-2k]","GbxHssFr [0.1-10]","GbxHssFr [10-2k]","GbxHssRr [0.1-10]","GbxHssRr [10-2k]","NacZdir [0.1-10]","NacXdir [0.1-10]"]     # Ubicacion de la fila que contiene el valor del parametro
    
    fig = plt.figure(figsize=[10,6])
    
    # Graficar los limites para cada 
    
    for i in range(0,15):
        jini=2*i
        jfinal=2*(i+1)
        
        X=X_NT_ISO[jini:jfinal]
        
        # Valor alerta
        
        X=X_NT_ISO[jini:jfinal]
        Y=Y_NT_ISO_ZonaBC[jini:jfinal]
        plt.plot(X, Y, color='green',  linestyle='--',linewidth=3)
        
        if i==0:
            plt.plot(X, Y, color='green', linestyle='--', label='ISOA-21 Zone B/C', linewidth=3)
    
        # Valor alarma
        
        X=X_NT_ISO[jini:jfinal]
        Y=Y_NT_ISO_ZonaCD[jini:jfinal]
        plt.plot(X, Y, color='red',  linestyle='--', linewidth=3)
        
        if i==0:
            plt.plot(X, Y, color='red', linestyle='--', label='ISOA-21 Zone C/D', linewidth=3)
    
    

        
    # Graficar los valores globales ISO 10816 (21)
    for i in range(0,16):
        Y=ValorNT_Med[i]
        X=Xt[i]
        #print(X, Y)
        plt.bar(X,Y, label=Nombre_NT[i])
        plt.legend()
        
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    P_Med2[Punto_Med_Select][2]
    plt.title(" WTG : "+P_Med2[Punto_Med_Select][0] +" Measurement date: " + P_Med2[Punto_Med_Select][2])
    plt.xlabel("Measurement point-parameter")
    plt.ylabel("Amplitude in "+ P_Med2[Punto_Med_Select][7])
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle(" Measurement of ISOA 10816 (21) vibration values" )
    plt.show()
    
    return




    #--------------------------------------------------------------------------



def Graficar_Descriptors():
    
     
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    X=[0]
    Y=[0]
    Xt=[1,2,3,4,5,6,7]

    fig = plt.figure(figsize=[10,6])
    for i in range(0,7):
        Y=ValorPT_Med[i]
        X=Xt[i]
        #print(X, Y)
        plt.bar(X,Y, label=Nombre_PT2[i])
        plt.legend()
       
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    P_Med2[Punto_Med_Select][2]
    plt.title(" WTG : "+P_Med2[Punto_Med_Select][0] +" Measurement date: " + P_Med2[Punto_Med_Select][2])
    plt.xlabel("Parameter")
    plt.ylabel("Value according to descriptors unit")
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle("Main Descriptors measurement values" )
    plt.show()
    
    
    return




    #--------------------------------------------------------------------------




def Graficar_Descriptors_Comparative():
    
     
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    X=[0]
    Y=[0]
    Xt=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

    fig = plt.figure(figsize=[10,6])
    j=0
    for i in range(0,7):
        Y=ValorPT_Med[i]
        X=Xt[j]
        #print(X, Y)
        plt.bar(X,Y, label=Nombre_PT2[i])
        plt.legend()
        
        #Descriptor referencia
        
        Y=ValorPT_Ref[i]
        X=Xt[j+1]
        #print(X, Y)
        plt.bar(X,Y, color='skyblue')
        if j==0:
            plt.bar(X,Y, color='skyblue', label="Baseline value")
            plt.legend()
            
        j=j+2
        
        
        
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    P_Med2[Punto_Med_Select][2]
    plt.title(" WTG : "+P_Med2[Punto_Med_Select][0] +" Measurement date: " + P_Med2[Punto_Med_Select][2]+ "Baseline measurement date :"+P_Ref2[Punto_Med_Select][2])
    plt.xlabel("Parameter")
    plt.ylabel("Value according to descriptors unit")
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle("Main Descriptors values from measurement and Baseline" )
    plt.show()
    
    return




    #--------------------------------------------------------------------------





def Graficar_NT_Comparativo():
    
     
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    V=[0]
    X=[0]
    Y=[0]
    Xt=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    fig = plt.figure(figsize=[10,6])
    
    for i in range(0,16):
    
        jini=2*i
        jfinal=2*(i+1)
    
        # Valor alerta
        
        X=X_NT_ISO[jini:jfinal]
        Y=Y_NT_ComparativoBC [jini:jfinal]
        plt.plot(X, Y, color='green', linestyle='--',linewidth=3)
        
        if i==0:
            plt.plot(X, Y, color='green', label='Increment-Alert',linestyle='--', linewidth=3)
    
        # Valor alarma
        
        X=X_NT_ISO[jini:jfinal]
        Y=Y_NT_ComparativoCD [jini:jfinal]
        plt.plot(X, Y, color='red',linestyle='--', linewidth=3)
    
        if i==0:
            plt.plot(X, Y, color='red', label='Increment - Alarm', linestyle='--', linewidth=3)
    
        
    
    
    for i in range(0,16):
        
        Y=ValorNT_Med[i]/ValorNT_Ref[i]
        X=Xt[i]
        #print(X, Y)
        plt.bar(X,Y, label=Nombre_NT[i])
        plt.legend()
       
   
    #Atributos
    # Todos se ponen despues que graficas 
    #de lo contrario son atributos no callables
    
    P_Med2[Punto_Med_Select][2]
    plt.title(" WTG : "+P_Med2[Punto_Med_Select][0] +" Measurement date: " + P_Med2[Punto_Med_Select][2] + "  Baseline measurement date: " + P_Ref2[Punto_Med_Select][2])
    plt.xlabel("Measurement point-parameter")
    plt.ylabel("Dimensionless")
    
    #ax[0].fig(figsize=9,6)
    
    plt.grid()
    
    
    #plt.style('dark_badgroung') the object is not callable
    #Cursor(ax[0], horizOn=True, vertOn=True, color='green', linewidth=2.0)
  
    plt.suptitle("Overall comparative analysis. Measurement / Baseline coefficient" )
    plt.show()
    
    
    return




    #--------------------------------------------------------------------------





def Graficar_Analizar():
    
    global Punto_Med_Select
    
    Punto_Med_Select = pointmed_selected
    
    #print("Graficar_analizar",Punto_Med_Select, method_selected)
    

    # 'Descriptors',, )    

    if method_selected==0:
        #  Overall 
        # Graficar_NT()
        Graficar_NT_Version2()
                 
    if method_selected==1:
        # 'Time waveform signal analysis'
        Graficar_TimeSignal()
    
    if method_selected==2:
        #  'Frequency analysis' 
        Graficar_Spectrum()
    
    if method_selected==3:
         #'Dual analysis (times waveform - frequency)
         Graficar_EspectroTimeSignal()
    
    if method_selected==4:
        # 'Comparative overall analysis'
        Graficar_NT_Comparativo()
        
    if method_selected==5:
         'Comparative frequency analysis'
         Graficar_Spectrum_MedRef()
        
    if method_selected==6:
        #  'Diagnostic frequency analysis'
        # Graficar_Spectrum_MedEntreRef()
        showinfo(title='', message='Next development') 
    
    if method_selected==7:
        #  'Descriptors'
        Graficar_Descriptors()
        
    if method_selected==8:
        # 'Dual analysis (Measurement and baseline spectrum)' 
        #showinfo(title='', message='Next development') 
        Graficar_EspectroMeasurementBaseline()
   
    if method_selected==9:
        # 'Comparative descriptors analysis'
        Graficar_Descriptors_Comparative()        
    
    if method_selected==10:
        # 'Comparative descriptors analysis'
        espectro_cascada2()        
    
    if method_selected==11:
        # 'Comparative descriptors analysis'
        sdp()   
    if method_selected==12:
        # 'Comparative descriptors analysis'
        phase()        
     
     

                                 
    #Graficar_EspectroTimeSignal()

    
    return




    #--------------------------------------------------------------------------




def Leer_PT_Med():
    
    #print('Parametros tecnologicos')
    
    B=0
    for i in range(0, 11):
        try:
            A=Valores[Fila_PT[i]]
            A=A[20: ]
            B=float(A)
            if i==0:
                B=B/1000   # onvertirlo en MW
            ValorPT_Med[i]=B
            
            #print(i,Valores[Fila_PT[i]],  ValorPT_Med[i])
        except:
            B=0
            #print (i, "error")
    
    return




    #--------------------------------------------------------------------------




def Leer_PT_Ref():
    
    #print('Parametros tecnologicos')
    
    B=0
    for i in range(0, 11):
        try:
            A=Valores_Ref[Fila_PT[i]]
            A=A[20: ]
            B=float(A)
            if i==0:
                B=B/1000 # convertirlo en MW
                
            ValorPT_Ref[i]=B
            
            #print(i,Valores_Ref[Fila_PT[i]],  ValorPT_REf[i])
        except:
            B=0
            #print (i, "error")
    
    
    return

  



    #--------------------------------------------------------------------------




def Leer_NT_Med():

    B=0
    for i in range(0, 24):
        try:
            A=Valores[Fila_NT[i]]
            A=A[20: ]
            B=float(A)
            ValorNT_Med[i]=B
            
            #print(i,Valores[Fila_NT[i]],  ValorNT_Med[i])
        except:
            B=0
            #print (i, Fila_NT[i], Valores[Fila_NT[i]],"error")
       
    return




    #--------------------------------------------------------------------------




def Leer_NT_Ref():
    
    B=0
    for i in range(0, 24):
        try:
            A=Valores_Ref[Fila_NT[i]]
            A=A[20: ]
            B=float(A)
            ValorNT_Ref[i]=B
            
            #print(i,Valores_Ref[Fila_NT[i]],  ValorNT_Ref[i])
        except:
            B=0
            #print (i, Fila_NT[i], Valores_Ref[Fila_NT[i]],"error")
    
    return

  



    #--------------------------------------------------------------------------



  
def LeerFichero_UFF_MedRef():
        Leer_FicheroUFF_Med()
        Leer_FicheroUFF_Ref()
        Leer_PT_Med()
        Leer_PT_Ref()
        Leer_NT_Med()
        Leer_NT_Ref()
        
        showinfo(title='', message='Process is finish. Select options to continium...') 
        
        Combobox_PuntoMed['state']='readonly'
        Combobox_Method['state']='readonly'
        
  
        return

    
#-----------------------------------------------------------------------------
#evaluacion de rodamiento
def evaluacion_rodamiento(data):
       
    #kurtosis

    Kurtosis=kurtosis(data)
    global ek

    if Kurtosis>2.9:
    
    
        ek='warning'
    
    elif Kurtosis>4.4:
    
       ek='danger'
    
    else:
    
    
       ek='good'

#skew

    Skew=skew(data)
    global es

    if Skew>1.6:
    
        es='good'
    else:
    
       es='danger'

#rms
   
    rms = np.sqrt(np.mean(data**2))
    global erms

    if rms>15:
  
        erms=('danger')
    else:
   
        erms='good'

#factor de cresta

    pico=data.max()
    fc=pico/rms

#encontrar picos
#plt.subplot(2,2,1)

    
    peaks2, _ = find_peaks(data, height=19) 
    peaks3, _ = find_peaks(data, threshold=3)  
    
    cant_picos1=len(peaks2)
    cant_picos2=len(peaks3)

    #plt.plot(peaks2, data[peaks2], "ob"); plt.plot(data); plt.legend(['severidad'])
    #plt.show()
    #plt.plot(peaks3, data[peaks3], "vg"); plt.plot(data); plt.legend(['impactos'])
    
    print(len(peaks2))
    print(len(peaks3))
    
    #plt.show()

#evaluacion final 

    if ek=='good' and es=='good' and erms=='good' and picos1==0 and picos2==0:
        evaluacion= 'good'
    elif ek=='danger' and es=='danger' and erms=='danger' and picos1 !=0 and picos2 !=0:
         evaluacion='danger'
    else:
         evaluacion='warning'
    
    return evaluacion

def evolvente(signal,t,N,dt):
    
    
    y = butter_lowpass_filter(data, cutoff, fs, order)
    
    
    
    
    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax0.plot(t, signal, label='signal')
    ax1.plot(t, amplitude_envelope, label='envelope')
    #ax1.plot(t[1:], instantaneous_frequency)
    ax1.set_xlabel("envolvente")
    fig.tight_layout()
    
     
     # graficar espectros
    #---------------------
    
    w=hann(N)   #Ventana hanning
    
    Yf= rfft(amplitude_envelope)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    
    
    for i in range(0,20):
       Yf[i]=Yf[20]
    
    #plt.figure(facecolor="black")   
    fig = plt.figure(figsize=[10,6])
    plt.plot(Xf, np.abs(Yf/Normalizado),color='skyblue')
    plt.show()
    
    return amplitude_envelope

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
    

def espectro_cascada(y,z1,z2):
    
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib.colors import colorConverter
    from mpl_toolkits.mplot3d.axes3d import Axes3D
    from datetime import datetime
    
    
    fig = plt.figure(figsize=(8,6))
    axes3d = Axes3D(fig)
    
    xs=[]
    for i in range(0, len(z2)):
        #fecha=fecha1.split("T")
        #fechaf="20"+fecha[0]
        #Fecha=datetime.strptime(fechaf, "%Y-%m-%d")
        
        xs.append(5)
        
    axes3d.plot(xs,y,z1)
    plt.plot(xs,z1)
      
    
    xs=[]
    for i in range(0, len(z2)):
       
        #fecha=fecha2.split("T")
        #fechaf="20"+fecha[0]
        #Fecha=datetime.strptime(fechaf, "%Y-%m-%d")
        xs.append(10)
   

    axes3d.plot(xs,y,z2)
    
    axes3d.set_ylabel('Frequency (Hz)')
    axes3d.set_zlabel('Magnitude')
   
def espectro_cascada2():
    
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib.colors import colorConverter
    from mpl_toolkits.mplot3d.axes3d import Axes3D
    from datetime import datetime
    
    N=int(P_Med2[2][3])  # Cantidad de muestras
    Fs=float(P_Med2[2][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    fig = plt.figure(figsize=[10,6])
    axes3d = Axes3D(fig)
    xs=[]
    xs1=[]
    xs2=[]
    xs3=[]
    xs4=[]
    xs5=[]
    xs6=[]
    xs7=[]
    xs8=[]
    
    Yt_Med=M_Med2[0]
    Yt_Med1=M_Med2[1]
    Yt_Med2=M_Med2[2]
    Yt_Med3=M_Med2[3]
    Yt_Med4=M_Med2[4]
    Yt_Med5=M_Med2[5]
    Yt_Med6=M_Med2[6]
    Yt_Med7=M_Med2[7]
    Yt_Med8=M_Med2[8]
    
    
    Yf= rfft(Yt_Med)[0:N]
    Yf1= rfft(Yt_Med1)[0:N]
    Yf2= rfft(Yt_Med2)[0:N]
    Yf3= rfft(Yt_Med3)[0:N]
    Yf4= rfft(Yt_Med4)[0:N]
    Yf5= rfft(Yt_Med5)[0:N]
    Yf6= rfft(Yt_Med6)[0:N]
    Yf7= rfft(Yt_Med7)[0:N]
    Yf8= rfft(Yt_Med8)[0:N]
    

    
    Xf= rfftfreq(N, dt)   
    Normalizado=N**0.5
   
    for i in range(0,20):
       Yf[i]=Yf[20]
    for i in range(0,20):
       Yf1[i]=Yf1[20]
    for i in range(0,20):
       Yf3[i]=Yf3[20]  
    
    for i in range(0,20):
       Yf4[i]=Yf4[20]
    for i in range(0,20):
       Yf5[i]=Yf5[20]
    for i in range(0,20):
       Yf6[i]=Yf6[20]
    for i in range(0,20):
       Yf7[i]=Yf7[20]
    for i in range(0,20):
       Yf8[i]=Yf8[20]
    
    
    
    y0=np.abs(Yf/Normalizado)
    y1=np.abs(Yf1/Normalizado)
    y2=np.abs(Yf2/Normalizado)
    y3=np.abs(Yf3/Normalizado)
    y4=np.abs(Yf4/Normalizado)
    y5=np.abs(Yf5/Normalizado)
    y6=np.abs(Yf6/Normalizado)
    y7=np.abs(Yf7/Normalizado)
    y8=np.abs(Yf8/Normalizado)
    
    for i in range(0, len(y0)):
        xs.append(5)
    axes3d.plot(xs,Xf,y0) 
    
    
    
    for i in range(0, len(y1)):
        xs1.append(10)
    axes3d.plot(xs1,Xf,y1)    
    
    
    for i in range(0, len(y3)):
        xs3.append(20)
    axes3d.plot(xs3,Xf,y3)    
    
    for i in range(0, len(y4)):
        xs4.append(25)
    axes3d.plot(xs4,Xf,y4)    
    
    for i in range(0, len(y5)):
        xs5.append(30)
    axes3d.plot(xs5,Xf,y5)    
    
    for i in range(0, len(y6)):
        xs6.append(35)
    axes3d.plot(xs6,Xf,y6)    
    
    for i in range(0, len(y7)):
        xs7.append(40)
    axes3d.plot(xs7,Xf,y7)    
    
    for i in range(0, len(y8)):
        xs8.append(45)
    axes3d.plot(xs8,Xf,y8)    
         
    
def sdp():
   
    from scipy import signal
     
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    global Xt
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    
    #print(Punto_Med_Select, M_Med2[Punto_Med_Select+2][262120], M_Med2[Punto_Med_Select+1][262135],M_Med2[Punto_Med_Select][262142])
    f, Pxx_spec = signal.periodogram(Yt_Med, Fs, 'flattop', scaling='spectrum')
    plt.figure()
    plt.semilogy(f, np.sqrt(Pxx_spec))
    plt.ylim([1e-4, 1e1])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Linear spectrum [V RMS]')
    plt.show()

    
    return

def phase():
    
    from scipy import signal
    # Datos iniciales
    #--------------
    
    N=int(P_Med2[Punto_Med_Select][3])  # Cantidad de muestras
    Fs=float(P_Med2[Punto_Med_Select][5])
    dt=1/Fs
    Fs=1/dt
    T=N*dt
   
    # Series de datos a graficar
    #----------------------------
    
    Xt=np.linspace(0,T,(N),endpoint=True)
    Yt_Med=M_Med2[Punto_Med_Select]
    Yt_Ref=M_Ref2[Punto_Med_Select]
    
    Yf= rfft(Yt_Med)[0:N]
    Xf= rfftfreq(N, dt)
    Normalizado=N**0.5
    yf = np.fft.fft(Yt_Med)
    
    
    for i in range(0,20):
       Yf[i]=Yf[20]
    
    #plt.figure(facecolor="black")   
    #fig = plt.figure(figsize=[10,6])
    #plt.plot(Xf, np.abs(Yf/Normalizado),color='skyblue')
    
    # Where is a 200 Hz frequency in the results?
    freq = np.fft.fftfreq(Xt.size, d=T)
   # index, = np.where(np.isclose(freq, 200, atol=1/(T*N)))

# Get magnitude and phase
    #magnitude = np.abs(Yt_Med[index[1]])
    #phase = np.angle(Yt_Med[index[1]])
    #print("Magnitude:", magnitude, ", phase:", phase)

# Plot a spectrum 
    plt.plot(freq[0:N//2], 2/N*np.abs(yf[0:N//2]), label='amplitude spectrum')   # in a conventional form
    plt.plot(freq[0:N//2], np.angle(yf[0:N//2]), label='phase spectrum')
    plt.legend()
    plt.grid()
    plt.show()
    
  
    
    return

    
#=============================================================================

# LLAMADAS A FUNCIONES PREPARATORIAS

#==============================================================================

CrearListas()
#==============================================================================

# CREACCION DE LA INTERFACE GRAFICA

#==============================================================================

root = Tk()
root.config(bg="black")
root.title("Aruna_Diagnostic oriented Vibration Analysis")

global method_selected
global Descrip_PMed, Descrip_PMed2


# Inicializar variables

frame= LabelFrame(root, text="", padx=150, pady=150, fg="white", bg="black")
frame.pack(padx=500, pady=300)


# Crear boton comando lectura fichero

# la funcion a la que llama el boton debe ser definida previamente
# En unn programa de verdad ponerla al principio

# Seleccionar ficheros
#----------------------

label_Action =Label(text="Select files to analysis and Baseline (Pattern)", bg="black", fg="white", width=35, anchor='e')
label_Action.place(x=40, y=20)

label_Nombrefichero =Label(text="", bg="gray", fg="white", width=100)
label_Nombrefichero.place(x=50, y=50)
label_Nombrefichero_Ref =Label(text="", bg="gray", fg="white", width=100)
label_Nombrefichero_Ref.place(x=50, y=80)

boton_FicheroMedicion=Button(root,text="File to analysis", width=15, command=SelectFichero, fg="white",bg="black")
boton_FicheroMedicion.place(x=770, y=50)

boton_FicheroRef=Button(root,text="Baseline files", width=15, command=SelectFicheroReferencia, fg="white",bg="black")
boton_FicheroRef.place(x=770, y=80)

boton_Aceptar=Button(root,text="Read files", width=10, command=LeerFichero_UFF_MedRef, fg="white",bg="black", pady=20)
boton_Aceptar.place(x=890, y=48)

# Seleccionar metodo de analysis
#-------------------------------

label_Method =Label(text="Select analysis method", bg="black", fg="white", width=18, anchor='e')
label_Method.place(x=40, y=110)

methods=('Overall values','Measurement / Baseline overall analysis','Descriptors','Comparative descriptors analysis' ,'Dual analysis (times waveform - frequency)','Time waveform signal analysis', 'Frequency analysis','Dual analysis (Measurement and baseline spectrum)', 'Comparative frequency analysis', 'Measurement / Baseline frequency analysis','Waterfall','specturn density frecuency','phase')   
selected_method=StringVar()
Combobox_Method=ttk.Combobox(root, textvariable=selected_method,width=40 )   # Construir combobox
Combobox_Method['values']=methods
Combobox_Method['state']='disable'
Combobox_Method.bind('<<ComboboxSelected>>', Method_Changed)
Combobox_Method.set('Overall values')
Combobox_Method.len=15
method_selected=0

Combobox_Method.place(x=50, y=140)

# Seleccionar punto de medicion
#-------------------------------

Descrip_PMed=["1- Generator Drive End  m/s2","2- Generator Non Drive End m/s2","3- High Speed Shaft     V","4- 1st Planetary Stage  m/s2","5- 2nd Planetary Stage  m/s2","6- Intermediate Speed Stage F m/s2","7- Intermediate Speed Stage R m/s2","8- High Speed Stage Fro m/s2","9- High Speed Stage Rea m/s2","10- Nacelle Z Direction  m/s2", "11- Nacelle X Direction  m/s2"]
Descrip_PMed2=["GnDE","GnNDE","HSS_v","PLT-1S","PLT-2S","ISS_F","ISS_R","HSS_F","HSS_R","NAC_Z", "NAC_X"]

Descrip_PRef=["1- Generator Drive End  m/s2","2- Generator Non Drive End m/s2","3- High Speed Shaft     V","4- 1st Planetary Stage  m/s2","5- 2nd Planetary Stage  m/s2","6- Intermediate Speed Stage F m/s2","7- Intermediate Speed Stage R m/s2","8- High Speed Stage Fro m/s2","9- High Speed Stage Rea m/s2","10- Nacelle Z Direction  m/s2", "11- Nacelle X Direction  m/s2"]
Descrip_PRef2=["GnDE","GnNDE","HSS_v","PLT-1S","PLT-2S","ISS_F","ISS_R","HSS_F","HSS_R","NAC_Z", "NAC_X"]
 
label_PuntoMed =Label(text="Select measurement point", bg="black", fg="white", width=21, anchor='e')
label_PuntoMed.place(x=40, y=170)

selected_Point=StringVar()
Combobox_PuntoMed=ttk.Combobox(root, textvariable=selected_Point,width=40)   # Construir combobox
Combobox_PuntoMed['values']=Descrip_PMed
Combobox_PuntoMed['state']='disable'
Combobox_PuntoMed.bind('<<ComboboxSelected>>', PointMed_Changed)
Combobox_PuntoMed.set("1- Generator Drive End  m/s2")
pointmed_selected=0

Combobox_PuntoMed.place(x=50, y=200)

# Graficar - Analizar 
# --------------------

# ejecuta diferentes opciones de graficos en funcion del metodo y el punto de medicion seleccionado

boton_GraficarAnalizar=Button(root,text="Graphics and Analysis ", width=25, command=Graficar_Analizar, fg="white",bg="black")

#boton_GraficarAnalizar.state='disable'

boton_GraficarAnalizar.place(x=70, y=240)





""" ***************************************************************************************

# Radiobutton

r=IntVar()
r.set("3")


radio_Boton1=Radiobutton(root, text="Mierda1  ",bg="gray", fg="white",variable=r, value=1, command=lambda: RadioButton_clicked(r.get())).place(x=340, y=360)
radio_Boton2=Radiobutton(root, text="Mierda2  ",bg="gray", fg="white",variable=r, value=2, command=lambda: RadioButton_clicked(r.get())).place(x=340, y=380)
radio_Boton3=Radiobutton(root, text="Mierda3  ",bg="gray", fg="white",variable=r, value=3, command=lambda: RadioButton_clicked(r.get())).place(x=340, y=400)

******************************************************************************************"""



mainloop()




    