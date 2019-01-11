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
    '''
    l1 = plt.plot(-5,-5, color = 'gray' , label = 'PPPC4DMID'                       , linewidth = 2)
    l2 = plt.plot(-5,-5, color = 'gray' , label = 'PPPC4DMID EW' , linestyle = '--' , linewidth = 2)
    l3 = plt.plot(-5,-5, color = 'gray' , label = 'MadDM',         linestyle = '--' , linewidth = 2)

    first_legend = plt.legend(handles=[l1[0],l2[0]], fontsize=SIZE-9, loc = [0.05,0.05], fancybox=True)
    frame = first_legend.get_frame()
    frame.set_edgecolor('gray')
    ax = plt.gca().add_artist(first_legend)
    '''
    handles = []
    for C in chans:
        x, y = np.loadtxt(n1n1 + '/10TeV_' + CR + '.dat' , unpack=True )
        x = [ math.pow(10,num) for num in x]
        print  len(x) , len(y)
        a = plt.plot(dic_noEW['x'] , dic_noEW[CR][DM][C] , color = 'black' , linestyle= '-' , linewidth = width , label = 'PPPC4DMID'    )
        b = plt.plot(dic_EW['x']   , dic_EW[CR][DM][C]   , color = 'black' , linestyle= '--', linewidth = width , label = 'PPPC4DMID EW' )

        handles.append( a[0] )
        handles.append( b[0] )
        
        c = plt.plot(x,y , color = 'lime', linestyle = '-' , lw = width, label =  r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0 \rightarrow ZZ$' )
        handles.append( c[0] )

        e, y = np.loadtxt(xdxd + '/10TeV_' + CR + '.dat' , unpack=True )
        e = plt.plot(x,y , color = 'blue', linestyle = '-' , lw = width, label =  r'MadDM $x_d x_d \rightarrow ZZ$' )
        handles.append( e[0] )

        e, y = np.loadtxt(xdxdX + '/10TeV_'+ CR + '.dat' , unpack=True )
        f = plt.plot(x,y , color = 'blue', linestyle = '--' , lw = width, label =  r'MadDM $x_d x_d  \rightarrow ZZ+X$' )
        handles.append( f[0] )

    second_legend = plt.legend(handles= handles, fontsize=SIZE-12, loc = 'upper right', fancybox=True , ncol = 1)
    frame = second_legend.get_frame()
    frame.set_edgecolor('gray')
    ax = plt.gca().add_artist(second_legend)
    
    # plotting the Fermi sensitivity only for gamma rays
    if CR == 'gammas':
             Fermi_limits = [[ 0.5/float(DM) , 0.5/float(DM)],[-0.1, 70]]
             plt.plot(Fermi_limits[0],Fermi_limits[1] , color = 'gray', linestyle = '--')
             Fermi_limits = [[ 500/float(DM) , 500/float(DM)],[-2, 70]]
             plt.plot(Fermi_limits[0],Fermi_limits[1] , color = 'gray', linestyle = '--')
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , 0.3, 'Fermi Sensitivity'  ,  rotation=90, fontsize = 13 , color ='gray' )
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , 0.013, r'$\longrightarrow$' , fontsize = 20 , color ='gray' )

    os.system('mkdir PLOTS')
    plt.savefig('PLOTS/n1n1ZZ/' + DM + '_' + CR + '_PPPC_Comparison_n1n1ZZ.pdf', bbox_inches='tight')
    plt.close()



# Load the Dictionary from the npy file  ### Tables[spectrum][mass][channel]
Dic_NoEW = np.load('PPPC_Tables_noEW.npy').item()
Dic_EW = np.load('PPPC_Tables_EW.npy').item()

#print Dic_NoEW['Particle_Spectra']

#['antiprotons', 'gammas', 'neutrinos_e', 'neutrinos_mu', 'neutrinos_tau', 'positrons']


DMs = ['10000.0']
CRs = ['gammas','positrons','neutrinos_e']
for m in DMs:
    for c in CRs:
        print 'Producing the plot for the CR: ' + c + ' for a DM candidate of ' + m + ' GeV'
        Plot(m, dic_EW = Dic_EW, dic_noEW = Dic_NoEW , CR = c)






