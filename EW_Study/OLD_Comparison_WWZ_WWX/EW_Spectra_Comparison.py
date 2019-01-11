import os,sys
import numpy as np
import math
import matplotlib
from matplotlib  import cm
from matplotlib import ticker
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def Apply_Plot_Properties(x_label = True, y_label = True):
      ### Plotting Part, same for each plot
      SIZE = 20
      THICK_LABEL_SIZE = 15
      if y_label: plt.ylabel(r'$\frac{dN}{dlogx}$'     , fontsize = SIZE)
      if x_label: plt.xlabel(r'$x= \frac{K}{m_{ \chi}}$'  , fontsize = SIZE)
      
      plt.xlim(0.00000007, 1)
      plt.ylim(0.01, 400)
      plt.yscale('log')
      plt.xscale('log')
      plt.tick_params(axis='both', which='major', labelsize=THICK_LABEL_SIZE, length=10, width=1.1, top='off', right='off')
      plt.tick_params(axis='both', which='minor', labelsize=THICK_LABEL_SIZE, length=7 , width=1.1, top='off', right='off')


def Plot_Comparison_WW(DM='', DIR = ''):
    # ex_test1000GeV_ww_lhe.dat
    
 SIZE = 17

 Dic_EW = np.load('../PPPC_Tables_EW.npy').item()
 Dic_noEW = np.load('../PPPC_Tables_noEW.npy').item()

 py8 =    ['ex', 'gx', 'nuex','numux','nutaux','px']
 tab =    ['positrons', 'gammas','neutrinos_e', 'neutrinos_mu', 'neutrinos_tau','antiprotons', ]
 pretty = ['positrons', r'$\gamma$' , r'$\nu_e$', r'$\nu_{\mu}$', r'$\nu_{\tau}$' , r'$ \bar p$' ]
 

 for spec_Tab, spec_Pythia,pr in zip (tab,py8,pretty):
    mass = r'$ m_{\chi} = \ ' + str(DM).replace('000.0','') +  ' \ [TeV]$'
    plt.text(0.00000015, 200, r'$\chi \chi \rightarrow W^+ W^-$     ' + mass                              , size=SIZE, ha="left", va="center",)
    plt.text(0.00000015, 90,  pr + ' Spectrum'                                                 , size=SIZE, ha="left", va="center",)


    Apply_Plot_Properties(x_label = True, y_label = True)
    
    #plt.title(spec_Tab + r' spectrum from $\chi \chi \rightarrow W^+ W^-$ annihilation', y = 1.03)

    TAB_width = 1.8
    # Data_DMDM_WW_ZZ_10TeV
    a,b = np.loadtxt( DIR + './Data_DMDM_WW_'+DM + '/'  + spec_Pythia + '_test1000GeV_ww_lhe.dat', unpack=True )
    c,d = np.loadtxt( DIR + './Data_DMDM_WW_Z_'+DM + '/'  + spec_Pythia + '_test1000GeV_ww_lhe.dat', unpack=True )
    e,f = np.loadtxt( DIR + './WW_X_'+DM + '/'  + spec_Pythia + '_test1000GeV_ww_lhe.dat', unpack=True )
    g,h = np.loadtxt( DIR + './WW_H_'+DM + '/'  + spec_Pythia + '_test1000GeV_ww_lhe.dat', unpack=True )


    y = [ math.pow(10,num) for num in a]
    
    aa = plt.plot(y, b , color = 'gold' , linestyle= '-', label = r'$\chi \chi \rightarrow W^+ W^-$ MadDM'      , linewidth = TAB_width-0.6 )
    bb = plt.plot(y, d , color = 'blue'  , linestyle= '--', label = r'$\chi \chi \rightarrow W^+ W^- Z$ MadDM '   , linewidth = TAB_width-0.6 )
    bb = plt.plot(y, h , color = 'cyan'  , linestyle= '--', label = r'$\chi \chi \rightarrow W^+ W^- H$ MadDM '   , linewidth = TAB_width-0.6 )

    cc = plt.plot(y, f , color = 'black' , linestyle= '-', label = r'$\chi \chi \rightarrow W^+ W^- X(h,W,Z) $ MadDM' , linewidth = TAB_width-0.6 )


    plot = plt.plot(Dic_EW['x']  , Dic_EW[spec_Tab][DM]['WW']     , color = 'gray'  , linestyle= '--' , linewidth = TAB_width , label = 'PPPC4DMID EW' )
    plot = plt.plot(Dic_noEW['x'], Dic_noEW[spec_Tab][DM]['WW']   , color = 'gray'  , linestyle= ':', linewidth = TAB_width , label = 'PPPC4DMID noEW' )



    plt.legend(fontsize = 10, loc = 'lower right')
    os.system('mkdir PLOTS')
    plt.savefig('PLOTS/'+str(DM)+'EW_CorrectionsComparison_W_Z_' +  spec_Tab + '.png' , bbox_inches='tight', dpi = 250 )
    plt.close()
        #os.system('mkdir PLOTS')
    #plt.savefig('PLOTS/MadDM_Spectra/' + DM + '_' + spectrum + '_Lepton_Leptons.png', bbox_inches='tight', dpi = 250 )



# Load the Dictionary from the npy file  ### Tables[spectrum][mass][channel]

Plot_Comparison_WW(DM = '10000.0', DIR = '')
Plot_Comparison_WW(DM = '100000.0', DIR = '')
Plot_Comparison_WW(DM = '1000.0', DIR = '')






