# SAMBA_ilum Copyright (C) 2024 - Closed source


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Observação:  Introduzir o vácuo original no arquivo POSCAR final
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import numpy as np
import shutil
import os
#--------------------------
import plotly.offline as py
import plotly.graph_objects as go
#--------------------------------
import scipy.interpolate as interp
from scipy.interpolate import griddata
#-------------------------------------
import matplotlib as mpl
from matplotlib import cm
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.colors as mcolors


#===================================================
# Extraindo informações ============================
#===================================================
file0 = np.loadtxt('energy_scan.txt', dtype=str)
file0.shape
#----------------------
date_shift = file0[:,0]
date_E = np.array(file0[:,1],dtype=float)
E_min  = min(date_E)
E_max  = max(date_E)
delta  = date_shift[np.argmin(date_E)]
#------------------------------------------
delta_min = delta.replace('_', ' ').split()
a1_min = delta_min[0]; a2_min = delta_min[1]; z_min = delta_min[2] 
#-----------------------------------------------------------------


#--------------------------------------
file = open('xyz-scan_direct.dat', "w")
#--------------------------------------
for i in range(len(date_shift)):
    VTemp = str(date_shift[i])
    VTemp = VTemp.replace('_', ' ')
    file.write(f'{VTemp} {((date_E[i] -E_min)*1000)/Area} \n')
#-----------
file.close()
#-----------


#-----------------------------------------
file = open('xyz-scan_cartesian.dat', "w")
#-----------------------------------------
for i in range(len(date_shift)):
    VTemp = str(date_shift[i])
    VTemp = VTemp.replace('_', ' ').split()
    Coord_X = ((float(VTemp[0])*A1x) + (float(VTemp[1])*A2x))
    Coord_Y = ((float(VTemp[0])*A1y) + (float(VTemp[1])*A2y))
    file.write(f'{Coord_X} {Coord_Y} {((date_E[i] -E_min)*1000)/Area} \n')
#-----------
file.close()
#-----------





#==========================================================
# Obtendo os vetores de rede A1 e A2 da Heteroestrutura ===
#==========================================================
poscar = open('POSCAR.0', "r")
#-----------------------------
VTemp = poscar.readline()
VTemp = poscar.readline();  param = float(VTemp)
VTemp = poscar.readline().split();  A1x = float(VTemp[0])*param;  A1y = float(VTemp[1])*param;  A1z = float(VTemp[2])*param
VTemp = poscar.readline().split();  A2x = float(VTemp[0])*param;  A2y = float(VTemp[1])*param;  A2z = float(VTemp[2])*param
VTemp = poscar.readline().split();  A3x = float(VTemp[0])*param;  A3y = float(VTemp[1])*param;  A3z = float(VTemp[2])*param
#-------------
poscar.close()
#-------------


#================================================
# Gerando o arquivo POSCAR deslocado no plano ===
#================================================
poscar = open('POSCAR.0', "r")
poscar_new = open('POSCAR_temp', "w") 
#------------------------------------
VTemp = poscar.readline()
poscar_new.write(f'{VTemp}')
VTemp = VTemp.split()
nions1 = int(VTemp[2]);  nions2 = int(VTemp[3])
#----------------------------------------------
for k in range(7 + nions1):
    VTemp = poscar.readline()
    poscar_new.write(f'{VTemp}')
#-------------------------------
for k in range(nions2):
    VTemp = poscar.readline().split()
    poscar_new.write(f'{float(VTemp[0]) + delta_X} {float(VTemp[1]) + delta_Y} {VTemp[2]} \n')
#---------------------------------------------------------------------------------------------
poscar.close()
poscar_new.close()
#-----------------


#===========================================================================
# Convertendo as coordenadas do arquivo POSCAR de cartesiano para direto ===
#===========================================================================
a = np.array([A1x, A1y, A1z])
b = np.array([A2x, A2y, A2z])
c = np.array([A3x, A3y, A3z])
T = np.linalg.inv(np.array([a, b, c]).T)  # Definindo a matriz de transformação
#------------------------------------------------------------------------------
poscar = open('POSCAR_temp', "r")
poscar_new = open('POSCAR', "w") 
#-------------------------------
for k in range(7):
    VTemp = poscar.readline()
    poscar_new.write(f'{VTemp}')
#------------------------
VTemp = poscar.readline()
poscar_new.write(f'Direct \n')


#----------------------------------------------------------------------------------------------------
# Convertendo as posições atomicas cartesianas de todos os átomos da Supercélula para a forma direta,
# e ajustando as posições dos átomos que se encontram fora da célula.
#--------------------------------------------------------------------
for k in range(nions1 + nions2):
    VTemp = poscar.readline().split()
    x = float(VTemp[0])
    y = float(VTemp[1])
    z = float(VTemp[2])    
    #----------------------
    r = np.array([x, y, z])        # Definindo o vetor posição cartesiano do átomo  
    #----------------------           
    f = np.dot(T, r)               # Calculando a correspondenre posição em coordenadas fracionárias
    for m in range(3):
        f = np.where(f < 0, f + 1, f)
        f = np.where(f > 1, f - 1, f)
    #-------------------------------- 
    for m in range(3):
        f[m] = round(f[m], 6)
        if (f[m] > 0.9999 or f[m] < 0.0001):
           f[m] = 0.0
    poscar_new.write(f'{f[0]} {f[1]} {f[2]} \n')
#-------------
poscar.close()
poscar_new.close()
#-----------------


os.remove('POSCAR_temp')


#=====================================================
info = open('info_xy-scan.dat', "w", encoding='utf-8')
info.write(f'====================================================== \n')
info.write(f'Displacement carried out over the 2nd material lattice   \n')
info.write(f'Displacement_XY = ({delta_X}, {delta_Y}) in Å \n')
info.write(f'Displacement_XY = ({delta_A1}*A1, {delta_A2}*A2) \n')
info.write(f'------------------------------------------------------ \n')
info.write(f'ΔE = {Delta_E_meV:.12f} meV/Å^2  or  {Delta_E_J:.12f} J/m^2 \n')
info.write(f'====================================================== \n')
info.close()
#===========
