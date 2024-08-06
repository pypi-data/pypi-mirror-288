# SAMBA_ilum Copyright (C) 2024 - Closed source


from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os


#==========================================================================
# Obtendo os vetores de rede da Heteroestrutura ===========================
#==========================================================================
poscar = open('POSCAR.0', "r")
#-----------------------------
VTemp = poscar.readline()
VTemp = poscar.readline();  param = float(VTemp)
VTemp = poscar.readline().split();  A1x = float(VTemp[0])*param;  A1y = float(VTemp[1])*param;  A1z = float(VTemp[2])*param
VTemp = poscar.readline().split();  A2x = float(VTemp[0])*param;  A2y = float(VTemp[1])*param;  A2z = float(VTemp[2])*param
VTemp = poscar.readline().split();  A3x = float(VTemp[0])*param;  A3y = float(VTemp[1])*param;  A3z = float(VTemp[2])*param
VTemp = poscar.readline()
VTemp = poscar.readline().split(); nions = 0
for i in np.arange(len(VTemp)):
    nions += int(VTemp[i])
#-------------
poscar.close()
#-------------


#==========================================================================
# Obtendo o fator percentual de multiplicação dos vetores de Rede =========
#==========================================================================
A1 = np.array([float(A1x), float(A1y), float(A1z)])*param;  module_a1 = float(np.linalg.norm(A1))
A2 = np.array([float(A2x), float(A2y), float(A2z)])*param;  module_a2 = float(np.linalg.norm(A2))
A3 = np.array([float(A3x), float(A3y), float(A3z)])*param;  module_a3 = float(np.linalg.norm(A3))
#------------------------------------------------------------------------------------------------
if (module_a1 <= module_a2):
   fator = ((module_a1 +passo)/module_a1) -1
   param_initial = module_a1;  vector = 'A1'
if (module_a2 <  module_a1):
   fator = ((module_a2 +passo)/module_a2) -1
   param_initial = module_a2;  vector = 'A2'
#-------------------------------------------


#===================================================
# Extraindo informações ============================
#===================================================
shutil.copy('energy_scan.txt', 'a-scan.dat')
#-------------------------------------------
file0 = np.loadtxt('a-scan.dat')
file0.shape
#-------------------
date_f  = file0[:,0]
date_E  = file0[:,1]
#--------------------
E_min   = min(date_E)
E_max   = max(date_E)
delta_f = date_f[np.argmin(date_E)]
a_opt   = delta_f*param_initial
#------------------------------
date_f  = date_f*param_initial
f_min   = min(date_f)
f_max   = max(date_f)


#--------------------------------------------------
shutil.copyfile(str(delta_f) + '/POSCAR', 'POSCAR')
shutil.copyfile(str(delta_f) + '/CONTCAR', 'CONTCAR')
#----------------------------------------------------


#=======================================
# Interpolando os dados do a-scan ======
#=======================================
n_d = 250
#--------
f = interp1d(date_f, date_E, kind='cubic')
x_interp = np.linspace(f_min, f_max, n_d)
y_interp = f(x_interp)


#===================================================
# Plot 2D ==========================================
#===================================================
fig, ax = plt.subplots()
plt.plot([a_opt, a_opt], [-1000.0, +1000.0], color = 'red', linestyle = '--', linewidth = 1.0, alpha = 1.0)
plt.plot(x_interp, y_interp, color = 'black', linestyle = '-', linewidth = 1.0)
plt.scatter(date_f, date_E, s=5, color = 'black')
plt.title('a-scan', fontsize=10)
plt.xlim((f_min, f_max))
#------------------------------
delta_E = abs(E_max -E_min)*0.1
#------------------------------
plt.ylim((E_min -delta_E, E_final +delta_E))
plt.xlabel('$a_optimized$(${\AA}$)')
plt.ylabel('$E(eV)$')
ax.set_box_aspect(1.25/1)
#----------------------------------------------------------------------
plt.savefig('a-scan.png', dpi = 600, bbox_inches='tight', pad_inches=0)
# plt.savefig('a-scan.pdf', dpi = 600, bbox_inches='tight', pad_inches=0)
# plt.savefig('a-scan.svg', dpi = 600, bbox_inches='tight', pad_inches=0)
# plt.savefig('a-scan.eps', dpi = 600, bbox_inches='tight', pad_inches=0)


#=====================================================
info = open('info_a-scan.dat', "w", encoding='utf-8')
info.write(f'============================================================================== \n')
info.write(f'Optimized lattice parameter: a = {a_opt} Å\n')
info.write(f'------------------------------------------------------------------------------ \n')
info.write(f'a_initial = {param_initial} Å (|{vector}|);  multiplication factor = {delta_f} \n')
info.write(f'============================================================================== \n')
info.close()
#===========
