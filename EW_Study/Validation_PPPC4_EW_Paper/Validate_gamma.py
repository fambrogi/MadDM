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


def Apply_Plot_Properties(x_label = True, y_label = True):
      ### Plotting Part, same for each plot
      SIZE = 25
      THICK_LABEL_SIZE = 20
      if y_label: plt.ylabel(r'$\frac{dN}{dlogx}$'     , fontsize = SIZE)
      if x_label: plt.xlabel(r'$x= \frac{K}{m_{ \chi}}$'  , fontsize = SIZE)
      plt.xlim(0.000007, 1)
      plt.ylim(0.01, 400)
      plt.yscale('log')
      plt.xscale('log')
      plt.tick_params(axis='both', which='major', labelsize=THICK_LABEL_SIZE, length=10, width=1.1, top='off', right='off')
      plt.tick_params(axis='both', which='minor', labelsize=THICK_LABEL_SIZE, length=7 , width=1.1, top='off', right='off')


######
import math
DM = 3000

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


samples = ['Res_new/n1n1_wwa_1TeV.txt',           'Res_new/n1n1_wwa_10TeV.txt' ,
	   'Res_new/n1n1_wwa_only_100k_1TeV.txt', 'Res_new/n1n1_wwa_only_100k_10TeV.txt',
	   'Res_new/n1n1_wwa_only_ch80_1TeV.txt', 'Res_new/nunu_wwa_10TeV.txt',

]


os.system('mkdir plots_new')

colors = ['red','gold','blue','limegreen']
lab_eq = 'arXiv:1001.3950 Eq. B62.a' 
label_massless = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan.(0.5GeV)'
label_80 = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan.(80 GeV)'

masses = [1000, 5000, 10000, 20000]
#######################################################################################
""" Calculate from analytical equation """
# calculating from analytical equation
x_eq = [0.001 + i*0.0005 for i in range (1998) ]
x_eq = [ x for x in x_eq if x < 1 and x> 0]
for dm,c in zip (masses, colors):
     y  = [ i*dna_dx(i, dm=dm) for i in x_eq ]
     if dm != 10000: DM = str(dm).replace('1000','1 TeV').replace('5000','5 TeV').replace('20000','20 TeV')
     if dm ==10000: DM = str(dm).replace('10000','10 TeV')
     plt.plot(x_eq , y , color = c, ls = ':', lw = 0.7)




SIZE = 15
### setting legends
handles = []
for dm,c in zip (masses, colors):
     if dm != 10000: DM = str(dm).replace('1000','1 TeV').replace('5000','5 TeV').replace('20000','20 TeV')
     if dm ==10000: DM = str(dm).replace('10000','10 TeV')
     plot = plt.plot([-1000,-1000] , [-1000,-1000], color = c, label = r"$m_{\tilde \chi _1 ^0}$=" + DM )
     handles.append(plot[0])
first_legend = plt.legend(handles= handles, fontsize=SIZE-9, loc = 'upper left', fancybox=True , ncol = 1)
frame = first_legend.get_frame()
frame.set_edgecolor('gray')
ax = plt.gca().add_artist(first_legend)


handles = []
plot1 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = lab_eq , ls = ':')
plot2 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = label_massless, ls = '--' , lw = 1.1)
plot3 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = label_80 , ls = '-' , lw = 1.1)


handles.append(plot1[0])
handles.append(plot2[0])
handles.append(plot3[0])
second_legend = plt.legend(handles= handles, fontsize=SIZE-9, loc = 'upper right', fancybox=True , ncol = 1)
frame = second_legend.get_frame()
frame.set_edgecolor('gray')
ax = plt.gca().add_artist(second_legend)








#######################################################################################
""" MadDM massless chargino """
samples_dir = 'Res_new/massless_chargino/'


SCALE = 3.5
X, edges = [],[] ### contains the x values and the y values (ready for plotting)

handles = []
for dm,c in zip(masses,colors):
    range_h = [0.01, 1]
    bins = 20
    val = []
    files = samples_dir + 'n1n1_wwa_DMTeV_chmassless.txt'
    files = files.replace('DM', str(dm).replace('000',''))
    fi = open(files, 'r').readlines()

    values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n = [ x/dm  for x in values if x] 
    h,e = np.histogram(values_n , bins = bins, range = range_h, density = True )
    edges.append(e)
    for h,b in zip(h,e):
        val.append(h*b/SCALE)

    if dm != 10000: DM = str(dm).replace('1000','1 TeV').replace('5000','5 TeV').replace('20000','20 TeV')
    if dm == 10000: DM = str(dm).replace('10000','10 TeV')
    plot = plt.plot(e[:len(val)], val, color = c , ls = '--' , lw = 1.1)
    handles.append(plot[0])
    #plt.scatter(e[:len(val)], val, color = c, label = label_massless + r"$m_{\tilde \chi _1 ^0}$=" + DM , s = 3)






#######################################################################################
""" MadDM 80 GeV chargino """

samples_dir = 'Res_new/chargino_80/'


SCALE = 3.5
masses = [1000]
X, edges = [],[] ### contains the x values and the y values (ready for plotting)
for dm,c in zip(masses,colors):
    range_h = [0.01, 0.999]
    bins = 20
    val = []
    files = samples_dir + '../n1n1_wwa_only_ch80_DMTeV.txt'
    files = files.replace('DM', str(dm).replace('000',''))
    fi = open(files, 'r').readlines()

    values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n = [ x/dm  for x in values if x and x < (dm-dm/2000)] 
    h,e = np.histogram(values_n , bins = bins, range = range_h, density = True )
    edges.append(e)
    for h,b in zip(h,e):
        val.append(h*b/SCALE)

    if dm != 10000: DM = str(dm).replace('1000','1 TeV').replace('5000','5 TeV').replace('20000','20 TeV')
    if dm == 10000: DM = str(dm).replace('10000','10 TeV')
    plt.plot(e[:len(val)], val, color = c, label = label_massless + r"$m_{\tilde \chi _1 ^0}$=" + DM , ls = '-' , lw = 1.1)
    #plt.scatter(e[:len(val)], val, color = c, label = label_80 + r"$m_{\tilde \chi _1 ^0}$=" + DM , s = 3)




#######################################################################################
""" Properties """
plt.title(r'$DM \ DM  \rightarrow W^- W^+ \gamma$', y=1.03)

axes = plt.subplot(111)
plt.xlim(0.009 , 1.1 )
plt.yscale('log')
plt.xscale('log')
plt.ylim(0.01, 2)
plt.ylabel(r'$xdN_{\gamma}/dx$')
plt.xlabel(r'x = E/$m_{DM}$')
plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.grid(which='major', linestyle='--', color = 'lightgray', lw = 1.05)
plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)
#plt.legend(loc = 'upper left', fontsize = 6)
plt.savefig('plots_new/Gammas_Validation.pdf', bbox_inches = 'tight')
plt.close()






'''
masses = [1000, 10000, 1000, 10000, 1000, 10000, 1000]
v = 6.5
scales = [v,v,v,v,v,v,y]
# histo properties
range_h = [0.01, 1]
bins = 25

X, edges = [],[] ### contains the x values and the y values (ready for plotting)
for s,dm,scale in zip(samples, masses, scales):
    val = []
    fi = open(s, 'r').readlines()
    values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n = [ x/dm  for x in values if x] 
    h,e = np.histogram(values_n , bins = bins, range = range_h, density = True )
    edges.append(e)

    for h,b in zip(h,e):
        val.append(h*b/scale)
    X.append(val)


# PLOT as paper




axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for tick in axes.xaxis.get_minor_ticks():
                tick.label.set_fontsize(5) 
                # specify integer or one of preset strings, e.g.
                #tick.label.set_fontsize('x-small') 
                tick.label.set_rotation('vertical')
for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(8) 
                tick.label.set_rotation('vertical')

# official line from paper
x_10, y_10 = np.loadtxt('10TeV_gamma.csv', unpack = True)
x_1 , y_1  = np.loadtxt('1TeV_gamma.csv' , unpack = True)
plt.plot(x_10, y_10, color = 'blue', label = r'Digitized $m_{DM}$=10 TeV' , ls = ':')
plt.plot(x_1, y_1  , color = 'red' , label = r'Digitized $m_{DM}$=1 TeV' , ls = ':')

 





# labels
l_1_noch  = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma, \ m_{\tilde \chi_1 ^0}=$ 1 TeV' 
l_10_noch = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma, \ m_{\tilde \chi_1 ^0}=$ 10 TeV'
l_1_c     = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan.(80GeV),  1 TeV'
l_10_c    = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan. 10 Tev'
l_nu_1    = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+ \gamma, \ CM=$ 1 TeV'  
l_nu_10   = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+ \gamma, \ CM=$ 10 TeV'  
l_nu_1_a   = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+, w^- w^+ \gamma, \ CM=$ 1 TeV' 
 
labels = [l_1_noch , l_10_noch, l_1_c, l_10_c , l_nu_1, l_nu_10, l_nu_1_a ]
colors = ['red','blue','red','blue','orange','cyan', 'lime']
styles = ['--','--','-','-','--','--',':']

for e,y,c,l,s in zip (edges,X,colors,labels,styles):
     plt.plot(e[:len(y)], y, color = c, label = l , ls = s)




'''

