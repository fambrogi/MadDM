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


'''
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

# Summary of the dictionary in the PPC Tables:
# keys of the dic: ['antiprotons', 'gammas', 'Masses', 'neutrinos_mu','positrons', 'Particle_Spectra', 'x', 'DM_Channels', 'neutrinos_e', 'neutrinos_tau']
# a['gammas']['5.0']['ee']
# channels: ['mumu', 'qq', 'tautau', 'bb', 'gammagamma', 'tt', 'gg', 'WW','cc', 'hh', 'ZZ', 'ee']
# a['x'] = values of the x variable , x = E_kin/m_DM

def Plot(DM, dic_EW = '', dic_noEW = '', CR = '', channel = ''):
    
    n1n1  = 'Data_n1n1ZZ_10TeV'
    xdxd  = 'Data_xdxdZZ_10TeV'
    xdxdX = 'Data_xdxdZZX_10TeV'
    
    Style_Dic = {   'positrons': r'$e^+$' , 'gammas': r'$ \gamma$' , 'neutrinos_e':r'$\nu _e$' ,
        
            'ee' :{ 'l': r'$e^+ e^-$'  , 'c': 'lime' },
            'WW' :{ 'l': r'$W^+ W^-$'  , 'c': 'gold'    },
            'qq' :{ 'l': r'$q \bar q$' , 'c': 'cyan'   },
            'tt' :{ 'l': r'$t \bar t$' , 'c': 'blue'   },
            'gg' :{ 'l': r'$g g$'      , 'c': 'navy'   },
            'hh' :{ 'l': r'$h h$'      , 'c': 'magenta'   },     }

    SIZE = 20

    label_CR      = Style_Dic[CR] + ' Energy Spectrum'

    #i,l = np.loadtxt(py8_File_Name + '_MUMU.dat'   , unpack=True )
    #a = [ math.pow(10,num) for num in a]
    # Apply general plot properties
    Apply_Plot_Properties(x_label = True, y_label = True)
    
    DM = str(DM)
    mass = str(DM).replace('5000.0',r'5 TeV').replace('500.0',r'500 GeV') .replace('50000.0',r'50 TeV')
    mass = str(DM).replace('10000.0',r'10 TeV').replace('500.0',r'500 GeV') .replace('50000.0',r'50 TeV')

    plt.text(0.000015, 200, r'$ m_{\chi}=$ ' + mass , size=SIZE-5, ha="left", va="center")
    plt.text(0.000015, 100 ,  r' $\chi\chi \rightarrow ZZ \ , \ X=(\gamma,h,W^+,W^-,Z)$    ' , size=SIZE-5, ha="left", va="center")
    plt.text(0.000015, 50, label_CR , size=SIZE-5, ha="left", va="center",)

    width = 1.6
    EW, noEW = '--' , '-'
    x = dic_EW['x']

    chans = ['ZZ']
   
    l1 = plt.plot(-5,-5, color = 'gray' , label = 'PPPC4DMID'                       , linewidth = 2)
    l2 = plt.plot(-5,-5, color = 'gray' , label = 'PPPC4DMID EW' , linestyle = '--' , linewidth = 2)
    l3 = plt.plot(-5,-5, color = 'gray' , label = 'MadDM',         linestyle = '--' , linewidth = 2)

    first_legend = plt.legend(handles=[l1[0],l2[0]], fontsize=SIZE-9, loc = [0.05,0.05], fancybox=True)
    frame = first_legend.get_frame()
    frame.set_edgecolor('gray')
    ax = plt.gca().add_artist(first_legend)

    os.system('mkdir PLOTS')
    plt.savefig('PLOTS/n1n1ZZ/' + DM + '_' + CR + '_PPPC_Comparison_n1n1ZZ.pdf', bbox_inches='tight')
    plt.close()
'''

######

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

    res = 0.01 * (first+second+third)
    return res


 


# Files
Z_Ma5_old = "Zboson_energy.txt"
Z_Ma5_schannel = "n1n1_wwz_onlyzschannel.txt"

ma = open(Z_Ma5_old, 'r').readlines()
ma5_values = [ x.replace("\n","") for x in ma if '3100' not in x and 'progress' not in x and x ]
ma5_values_cleaned = [ eval(x) for x in ma5_values if x]
ma5_values_old = [ eval(x)/DM for x in ma5_values if x and x !=0]


ma_s = open(Z_Ma5_schannel, 'r').readlines()
ma5_values = [ x.replace("\n","") for x in ma_s if '3100' not in x and 'progress' not in x and x ]
ma5_values_cleaned_s = [ eval(x) for x in ma5_values if x]
ma5_values_schannel = [ eval(x)/DM for x in ma5_values if x and x !=0]


Z_yellow = "Z_paper_yellow.txt"
x,y, = np.loadtxt(Z_yellow, unpack = True)


bins = 50



# calculating from analytical equation
x_eq = [0.001 + i*0.0005 for i in range (1998) ]
y_eq = [ dnz_dx(i, dm=DM) for i in x_eq ] 


y_eq_100TeV  = [ dnz_dx(i, dm=100000) for i in x_eq ] 


# digitized plot
plt.plot(x,y, color = 'yellow', label = 'Paper (Digitized plot)')
# analytical plot
plt.plot(x_eq, y_eq ,        label =r"Eq. B.64 ($m_{\tilde \chi_1 ^0}$= 3 TeV)" , color = 'red' )
plt.plot(x_eq, y_eq_100TeV , label =r"Eq. B.64 ($m_{\tilde \chi_1 ^0}$= 100 TeV)" , color = 'orange' )

# old (with t-channels charginos, higgses)
plt.hist(ma5_values_old,      bins, histtype="step", color = 'blue', label = 'MadDM (with ch1 t-chan.)' , normed = True)
# old ( only s-channel Zs)
plt.hist(ma5_values_schannel, bins, histtype="step", color = 'lime', label = 'MadDM (only z s-chan.)' , normed = True)


# properties
plt.yscale('log')
plt.xscale('log')
plt.xlim(0.009,1.1)
plt.ylim(0.01,3.1)

majorLocator = MultipleLocator(20)
majorFormatter = FormatStrFormatter('%d')
minorLocator = MultipleLocator(5)
axes = plt.subplot(111)
axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))


for tick in axes.xaxis.get_minor_ticks():
                tick.label.set_fontsize(5) 
                # specify integer or one of preset strings, e.g.
                #tick.label.set_fontsize('x-small') 
                tick.label.set_rotation('vertical')
for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(8) 
                tick.label.set_rotation('vertical')

plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.grid(which='major', linestyle='--', color = 'lightgray', lw = 1.05)
plt.grid(which='minor', linestyle=':', color = 'lightgray', lw = 1.05)


plt.legend(loc = 'lower right' , fontsize = 9)
plt.xlabel(r"$x = \frac{E}{m_{DM}} $")

plt.ylabel("Normalized Counts /"+str(bins)+'GeV')

plt.savefig('histo_comparison.pdf', bbox_inches = 'tight')

plt.close()



# ma5_values_cleaned_s
bins = 50
axes = plt.subplot(111)
axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
plt.hist(ma5_values_cleaned,  bins, histtype="step", color = 'blue',   label = 'MadDM (with ch1 t-chan.)' , density = False)
plt.hist(ma5_values_cleaned_s,  bins, histtype="step", color = 'lime', label = 'MadDM (only z s-chan.)' , density = False)
plt.xlim(0 , 3100)
plt.ylim(0 , 5000)
plt.ylabel("Normalized Counts /"+str(bins)+'GeV')
plt.xlabel("Z energy [GeV]")
plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.legend(loc = 'upper left', fontsize = 10)
plt.savefig('simple_histo.pdf', bbox_inches = 'tight')
plt.close()

