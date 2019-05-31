import os,sys
import numpy as np
import math
import matplotlib
from matplotlib  import cm
from matplotlib import ticker
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
plt.rcParams['text.latex.preamble'] = [
                                       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
                                       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
                                       r'\usepackage{helvet}',    # set the normal font here
                                       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
                                       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
                                       ]
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

######
import math

def dna_dx(x, dm=1.0):
    alpha_em = 1/137.
    e = 80.3/dm
    factor = alpha_em / np.pi
    first = 4*(1-x+x**2)**2/(x*(1-x))*np.log(2/e)  
    second = 2*( 4 -12*x + 19*x**2 -22*x**3 +20*x**4 -10*x**5 +2*x**6)/((x-2)**2 * (x-1)*x)
    third = np.log(1-x)*(-6*x**5 + 32*x**4-74*x**3+84*x**2-48*x+16)/( (x-2)**3 * (x-1) * x )
    res = factor*(first + second + third)
    #print x, first, second, third
    return res


def theory_line(dm):
    """ x and y theory lines """
    x_eq = [0.001 + i*0.0005 for i in range (2050) ]
    x_eq = [ x for x in x_eq if x < 1 and x> 0]
    y  = [ i*dna_dx(i, dm=dm) for i in x_eq ]
    return x_eq, y

os.system('mkdir plots_new')

colors = ['red','gold','blue','limegreen']
lab_eq = 'arXiv:1001.3950 Eq. B62.a' 
label_massless = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan.(0.5GeV)'
label_80 = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan.(80 GeV)'
masses = [1000,20000,50000,100000]

#######################################################################################
# PLOTS

SIZE = 15

### setting legends
handles = []
for dm,c in zip (masses, colors):
     if dm != 10000: DM = str(dm).replace('1000','1 TeV').replace('5000','5 TeV').replace('20000','20 TeV')
     if dm ==10000: DM = str(dm).replace('10000','10 TeV')
     plot = plt.plot([-1000,-1000] , [-1000,-1000], color = c, label = r"$E_{CM}(\tilde \chi _1 ^0)$=" + DM )
     handles.append(plot[0])
first_legend = plt.legend(handles= handles, fontsize=SIZE-9, loc = 'upper left', fancybox=True , ncol = 1)
frame = first_legend.get_frame()
frame.set_edgecolor('gray')
ax = plt.gca().add_artist(first_legend)


handles = []
plot1 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = lab_eq , ls = ':')
plot3 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = label_80 , ls = '-' , lw = 1.1)


handles.append(plot1[0])
handles.append(plot3[0])
second_legend = plt.legend(handles= handles, fontsize=SIZE-9, loc = 'upper right', fancybox=True , ncol = 1)
frame = second_legend.get_frame()
frame.set_edgecolor('gray')
ax = plt.gca().add_artist(second_legend)



#######################################################################################
""" MadDM 80 GeV chargino """

samples_dir = 'Res_new/chargino_80/'

SAMPLES = {1000:'n1n1_wwa_only_ch80_1TeV.txt' , 20000:'n1n1_wwa_100k_20TeV_ch80_n0.txt', 50000:'n1n1_wwa_200k_50TeV_ch80_n78_cut500.txt' , 100000:'n1n1_wwa_200k_100TeV_ch80_n78_cut500.txt' }

original = []
SCALE = 3.5
X, edges = [],[] ### contains the x values and the y values (ready for plotting)

for dm,c in zip(masses,colors):

    if dm != 10000 and dm !=100000: DM = str(dm).replace('1000','1 TeV').replace('5000','5 TeV').replace('20000','20 TeV')
    if dm == 10000: DM = str(dm).replace('10000','10 TeV')
    if dm == 100000: DM = str(dm).replace('100000','100 TeV')

    ###### theory
    x,y = theory_line(dm)
    plt.plot(x , y , color = c, ls = ':', lw = 0.7)

    ###### MG5 histo 
    range_h = [0.00001, 2]
    bins = 500

    val = []
    files = samples_dir+ '/' + SAMPLES[dm]
    fi = open(files, 'r').readlines()

    values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n = [ x/dm  for x in values if x ] 
    original.append(values)
    h,e = np.histogram(values_n ,range = range_h, density = True )

    for h,b in zip(h,e):
        val.append(h*b/SCALE)

    plt.plot(e[:len(val)], val, color = c, label = label_massless + r"$m_{\tilde \chi _1 ^0}$=" + DM , ls = '-' , lw = 1.1)

#######################################################################################
""" Properties """									
#######################################################################################
plt.title(r'$DM \ DM  \rightarrow W^- W^+ \gamma$', y=1.03)

axes = plt.subplot(111)
axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))

plt.xlim(0.009 , 2 )
plt.yscale('log')
plt.xscale('log')
plt.ylim(0.01, 2)
plt.ylabel(r'$xdN_{\gamma}/dx$')
plt.xlabel(r'x = $E_{\gamma}$/$m_{DM}$')
plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
#plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)
#plt.legend(loc = 'upper left', fontsize = 6)
plt.savefig('plots_new/Gammas_Validation_ch80.pdf', bbox_inches = 'tight')
plt.close()


### simple histogram normalized by the mass
bins = 200
plt.title(r'$DM \ DM  \rightarrow W^- W^+ \gamma$', y=1.03)
plt.xlim(20000 , 100001)
plt.yscale('log')
plt.xscale('log')
#plt.ylim(0.01, 10)
plt.ylabel(r'$dN_{\gamma}/dx$')
plt.xlabel(r'x = $E_{\gamma}$/$m_{DM}$')
plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
plt.hist(original, bins= bins, color = colors, histtype = 'step', label = ['1 TeV','20 TeV','50 TeV','100 TeV'], density = True)
plt.legend()
plt.savefig('plots_new/simple_Gammas.pdf', bbox_inches = 'tight')
plt.close()


