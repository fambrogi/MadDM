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

import math
DM = 3000

def dnz_dx(x, dm = ''):
    alpha2 = 1
    pi = math.pi
    cw = 1
    mw = 80.3
    e = mw/dm
    factor = alpha2/pi * cw**2
    first =   (9*x**4 - 18*x**3 + 25*x**2 -16*x +8 )/(2*x*(1-x)) * math.log( (2*x/e) / (math.sqrt(1-x+x**2) ) ) 
    second =  2*( -3*x**5 + 16*x**4 -37*x**3 +42*x**2 -24*x +8)/( (2-x)**3 * (1-x) *x  ) * math.log(1-x)
    third = -(52 - 176*x + 271*x**2 -247*x**3 + 150*x**4 -55*x**5 +9*x**6)*x/(2*(2-x)**2 * (1-x)*(1-x+x**2) )
    res = 0.005 * (first+second+third)
    return res

def theory_line(dm):
    """ x and y theory lines """
    x_eq = [0.001 + i*0.0005 for i in range (2050) ]
    x_eq = [ x for x in x_eq if x < 1 and x> 0]
    y  = [ dnz_dx(i, dm=dm) for i in x_eq ]
    return x_eq, y






# *************************************************************************************************************************************************
# Files

range_h = [0.001, 1]
bins = np.logspace(np.log10(range_h[0]), np.log10(range_h[1]), 50)
print bins 
scale = 0.17


M = [1000,3000,10000]
C = ['blue', 'lime', 'gold']
L = ['1 TeV', '3 TeV', '20 TeV']

SIZE = 15
lab_eq = 'arXiv:1009.0224 Eq. B.62b' 
label_massless = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ z$ , $\tilde \chi_1 ^0 \sim \tilde \chi_1 ^{\pm}\sim$ 0.5 GeV'

handles = []
for dm,c,l in zip(M,C,L):
        x_eq, y_eq = theory_line(dm)
	plt.plot(x_eq, y_eq, color = c, ls = '--')

	F = open('Res/wwz/wwz_'+str(dm)+'.txt' , 'r').readlines()
        fi = F[15:-15] # remove the text lines
	values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
        values_n = [ x/dm  for x in values if x] 

        a = plt.hist(values_n, bins = bins, range = range_h, histtype = 'step', color = c, label = r'$E_{CM}$=' +l , density = True )




handles = []
plot1 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = lab_eq , ls = ':')
plot2 = plt.plot([-1000,-1000] , [-1000,-1000], color = 'black', label = label_massless, ls = '--' , lw = 1.1)

'''
handles.append(plot1[0])
handles.append(plot2[0] )
sec_legend = plt.legend(handles= handles, fontsize=SIZE-9, loc = 'upper left', fancybox=True , ncol = 1)
frame = sec_legend.get_frame()
frame.set_edgecolor('gray')
ax = plt.gca().add_artist(sec_legend)
'''

plt.legend(loc = 'upper right' , fontsize = 8)

os.system('mkdir Plots')
plt.xlim(0.009 , 2 )
plt.yscale('log')
plt.xscale('log')
plt.ylim(0.01, 50)
plt.ylabel(r'$dN_{z}/dx$')
plt.xlabel(r'x = $E_{z}$/$E_{CM}$')
plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
#plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)
#plt.legend(loc = 'upper left', fontsize = 6)
plt.savefig('Plots/n1n1_wwz.pdf', bbox_inches = 'tight')
plt.close()

















