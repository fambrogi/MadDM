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
    y  = [ dna_dx(i, dm=dm) for i in x_eq ]
    return x_eq, y






# *************************************************************************************************************************************************
# Files

range_h = [0.0001, 1]
bins = np.logspace(np.log10(range_h[0]), np.log10(range_h[1]), 100)
print bins 
scale = 0.17


M = ["1000","1000"]
C = ['blue', 'cyan']


SIZE = 15
lab_eq = 'arXiv:1009.0224 Eq. B.62b' 
label = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ z$'



 




FF_1 = 10
FF_10 = 3
handles = []
for el in [1]:

        x_eq, y_eq = theory_line(eval("1000"))
	plt.plot(x_eq, FF_1 * np.array(y_eq), color = 'red', ls = '--', label = 'arXiv 1009.0224 Eq.B62(b) 1 TeV'  )

        x_eq, y_eq = theory_line(eval("10000"))
	plt.plot(x_eq, FF_10 * np.array(y_eq), color = 'blue', ls = '--', label = 'arXiv 1009.0224 Eq.B62(b) 10 TeV'  )

	F = open('res/n1n1_wwa_1000.txt' , 'r').readlines()
        fi = F[15:-15] # remove the text lines
	values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
        values_n = [ x/1000.  for x in values if x] 
        a = plt.hist(values_n, bins = bins, range = range_h, histtype = 'step', color = 'orange', label = r'$ m_{\tilde \chi ^0 _1 } =$ 1 TeV'  , density = True )


	F = open('res/n1n1_wwa_10000.txt' , 'r').readlines()
        fi = F[15:-15] # remove the text lines
	values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
        values_n = [ x/10000.  for x in values if x] 
        a = plt.hist(values_n, bins = bins, range = range_h, histtype = 'step', color = 'cyan', label = r'$ m_{\tilde \chi ^0 _1 } =$ 10 TeV'  , density = True )


	plt.legend(loc = 'upper right' , fontsize = 9)


	os.system('mkdir Plots')
	plt.xlim(0.0009 , 3 )
	plt.yscale('log')
	plt.xscale('log')

	plt.ylabel(r'$dN_{\gamma}/dx$')
	plt.xlabel(r'x = $E_{\gamma}$/$E_{CM}$')
	plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
	plt.grid(which='minor', linestyle=':', color = 'lightgray', lw = 1.05)
	#plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)
	#plt.legend(loc = 'upper left', fontsize = 6)
	plt.savefig('Plots/n1n1_wwa.pdf', bbox_inches = 'tight')
	plt.close()

















