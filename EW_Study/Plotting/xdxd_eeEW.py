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


def READ(F):
    x, y = np.loadtxt(F , unpack=True )
    x = [ math.pow(10,num) for num in x]

    return x,y



def Apply_Plot_Properties(x_label = True, y_label = True):
      ### Plotting Part, same for each plot
      SIZE = 20
      THICK_LABEL_SIZE = 17
      if y_label: plt.ylabel(r'$\frac{dN}{dlogx}$'     , fontsize = SIZE)
      if x_label: plt.xlabel(r'$x= \frac{K}{m_{ \chi}}$'  , fontsize = SIZE)
      plt.xlim(0.000001, 1)
      plt.ylim(0.01, 700)
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
    DM_o = DM
    DM = str(DM).replace('1000.0','1').replace('10000.0','10').replace('100000.0','100')
    
    dir = '../Spectra/' + DM + 'TeV_ALL'
    Style_Dic = {   'positrons': r'$e^+$' ,
                    'gammas': r'$ \gamma$' ,
                    'neutrinos_e':r'$\nu _e$' ,
                    'neutrinos_mu':r'$\nu _{\mu}$' ,
                    'neutrinos_tau':r'$\nu _{\tau}$' ,
                    'antiprotons':r'$\bar p$' }
 
    Name_Dic = { 'positrons':'ex' , 'neutrinos_mu':'numux' , 'neutrinos_e':'nuex' , 'gammas':'gx' , 'antiprotons':'px' ,'neutrinos_tau':'nutaux' }
    
    
    
    SIZE = 18

    label_CR      = Style_Dic[CR] + ' Energy Spectrum'

    #i,l = np.loadtxt(py8_File_Name + '_MUMU.dat'   , unpack=True )
    #a = [ math.pow(10,num) for num in a]
    # Apply general plot properties
    Apply_Plot_Properties(x_label = True, y_label = True)
    
    DM = str(DM)


    plt.text(0.000002, 400 ,  r' $\chi _D\chi _D \rightarrow  e^- e^+ $ + Corr.    ' , size=SIZE-5, ha="left", va="center" , color = 'red')
    plt.text(0.000002, 180, r'$ m_{\chi _D}=$ ' + DM + ' TeV' , size=SIZE-5, ha="left", va="center" , color = 'blue')
    plt.text(0.000002, 100, label_CR , size=SIZE-5, ha="left", va="center", color = 'blue')

    width = 1.1
    EW, noEW = '--' , '-'
    x = dic_EW['x']

    chans = ['ee']

    handles = []
    
    spec = Name_Dic[CR]
    
    for C in chans:
        
        a = plt.plot(dic_noEW['x'] , dic_noEW[CR][DM_o][C] , color = 'black'  , linestyle= '--' , linewidth = width+0.2 , label = 'PPPC4DMID'    )
        b = plt.plot(dic_EW['x']   , dic_EW[CR][DM_o][C]   , color = 'black'  , linestyle= '-', linewidth = width+0.2 , label = 'PPPC4DMID EW' )

        ew_WZ          = 'Data_eeEW/Data_xdxd_ee_EW_' + DM + 'TeV/'   + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'
        ew_WZ_noPy8    = 'Data_eeEW/Data_xdxd_ee_EW_'+ DM + 'TeV_noPy8Weak/'   + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'
        ew_noWZ        = 'Data_eeEW/Data_xdxd_eenoEW_' + DM + 'TeV/'   + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'
        ew_noWZ_noPy8  = 'Data_eeEW/Data_xdxd_eenoEW_' + DM + 'TeV_noPy8Weak/'   + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'

        mssm_ee        = 'Data_eeEW/Data_n1n1_ee_' + DM + 'TeV/'   + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'
        mssm_ee_noPy8  = 'Data_eeEW/Data_n1n1_ee_' + DM + 'TeV_noPy8Weak/'   + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'

        plt.grid(color = "lightgray", linestyle=':')

        x,y = READ(ew_WZ)
        e = plt.plot(x , y     , color = 'magenta' , linestyle= '-', linewidth = width , label = r'$x_dx_d>ee$ + MG Corr. + Py8 EW' )

        x,y = READ(ew_WZ_noPy8)
        e = plt.plot(x , y     , color = 'magenta' , linestyle= '--', linewidth = width , label = r'$x_dx_d>ee$ + MG Corr.' )

        x,y = READ(ew_noWZ)
        d = plt.plot(x , y     , color = 'dodgerblue' , linestyle= '-', linewidth = width , label = r'$x_dx_d>ee$ + Py8 EW' )

        x,y = READ(ew_noWZ_noPy8)
        d = plt.plot(x , y     , color = 'dodgerblue' , linestyle= '--', linewidth = width , label = r'$x_dx_d>ee$' )


        x,y = READ(mssm_ee)
        e = plt.plot(x , y     , color = 'lime' , linestyle= '-', linewidth = width , label = r'$n_1n_1>ee$ + Py8 EW' )

        x,y = READ(mssm_ee_noPy8)
        e = plt.plot(x , y     , color = 'lime' , linestyle= '--', linewidth = width , label = r'$n_1n_1>ee$' )



    plt.legend(fancybox = True, loc = 'upper right', fontsize = SIZE- 12)
    # plotting the Fermi sensitivity only for gamma rays
    if CR == 'gammas':
             Fermi_limits = [[ 0.5/float(DM) , 0.5/float(DM)],[-0.1, 70]]
             plt.plot(Fermi_limits[0],Fermi_limits[1] , color = 'gray', linestyle = '--')
             Fermi_limits = [[ 500/float(DM) , 500/float(DM)],[-2, 70]]
             plt.plot(Fermi_limits[0],Fermi_limits[1] , color = 'gray', linestyle = '--')
             place = 0.3
             if DM == '1': place = 10
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , place, 'Fermi Sensitivity'  ,  rotation=90, fontsize = 13 , color ='gray' )
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , 0.013, r'$\longrightarrow$' , fontsize = 20 , color ='gray' )


    os.system('mkdir PLOTS')
    os.system('mkdir PLOTS/xdxd_eeEW')

    plt.savefig('PLOTS/xdxd_eeEW/' + DM + '_' + CR + '_eeEW_'+DM +'.pdf', bbox_inches='tight')
    plt.close()


# Load the Dictionary from the npy file  ### Tables[spectrum][mass][channel]
Dic_NoEW = np.load('../PPPC_Tables_noEW.npy').item()
Dic_EW = np.load('../PPPC_Tables_EW.npy').item()

#print Dic_NoEW['Particle_Spectra']

#['antiprotons', 'gammas', 'neutrinos_e', 'neutrinos_mu', 'neutrinos_tau', 'positrons']


DMs = ['1000.0','10000.0','100000.0']
CRs = ['gammas','positrons','neutrinos_e', 'neutrinos_tau' , 'neutrinos_mu' , 'antiprotons' ]
#CRs = ['gammas',]

for m in DMs:
    for c in CRs:
        print 'Producing the plot for the CR: ' + c + ' for a DM candidate of ' + m + ' GeV'
        Plot(m, dic_EW = Dic_EW, dic_noEW = Dic_NoEW , CR = c)






