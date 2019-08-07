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

# *************************************************************************************************************************************************
# Files

range_h = [0.01, 1]
#bins = np.logspace(np.log10(range_h[0]), np.log10(range_h[1]), 50)
bins  = 50
print bins 




C = ['blue', 'slateblue', 'cyan', 'lime',  'gold'  , 'orange', 'magenta', 'black']




mass_neu = r'$ m_{\tilde \chi_1 ^0}$='
SIZE = 20
lab_eq = 'arXiv:1009.0224 Eq. B.62b' 



handles = []
R = ['101','2']
S = ['-','--']
C = ['lime','blue']

luca = r'$ \chi _r \chi_r \rightarrow u \bar u $'

bos = { 'z':r'$z$' , 'a':r'$\gamma$' } 


mssm = r'$ \tilde \chi _1 ^0 \tilde \chi _1 ^0  \rightarrow u \bar u $' 
A = [r'x = $E_{\gamma}$/$E_{CM}$',r'x = $E_{z}$/$E_{CM}$']
Y = [r'$dN_{\gamma}/dx$', r'$dN_{z}/dx$']

for w,a,ya in zip (['a','z'] , A, Y ):
    for c,r,s in zip(C,R,S):


	F = open('res/Luca/Luca_qq' + w + '_' + r + '.txt' , 'r').readlines()
        fi = F[15:-15] # remove the text lines
	values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and 'particle' not in x and x !="\n" ]
        values_n = [ x/10000.  for x in values if x] 
        plt.hist(values_n, bins = bins, range = range_h, histtype = 'step', color = 'lime', label = luca + bos[w] + ', r=' + r.replace('101','1.01') , density = True , ls = s )


	F = open('res/Luca/MSSM_qq' + w + '_'  + r + '.txt' , 'r').readlines()
        fi = F[15:-15] # remove the text lines
	values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and 'particle' not in x and x !="\n"]
        values_n = [ x/10000.  for x in values if x] 
        plt.hist(values_n, bins = bins, range = range_h, histtype = 'step', color = 'blue', label = mssm + bos[w] + ', r=' + r.replace('101','1.01') , density = True , ls = s)


   
        x,y = np.loadtxt('res/Luca/qq' + w + '_' + r + '.csv', unpack = True)
        y = 30 * y
 	plt.plot(x,y, color = 'gray', label = 'MadDM Paper'  + ', r=' + r.replace('101','1.01') , ls = s , lw = 0.9)

        plt.ylabel(ya)
        plt.xlabel(a)

    plt.legend(loc = 'upper left' , fontsize = 7)
    plt.title( r'$ m_{\chi}=10$ TeV', y = 1.03 )
    os.system('mkdir Plots')
    plt.xlim(0 , 1.05 )
    #plt.yscale('log')
    #plt.xscale('log')
    plt.ylim(0., 4)
 
    plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
    #plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)
    #plt.legend(loc = 'upper left', fontsize = 6)
    
    plt.savefig('Plots/Luca_' + w + '.pdf', bbox_inches = 'tight')
    plt.close()

















