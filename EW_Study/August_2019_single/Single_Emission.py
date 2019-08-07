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

def Plot(DM, dic_EW = '', dic_noEW = '', CR = '', channel = '' , scaled = False):
    DM_o = DM
    DM = str(DM).replace('1000','1').replace('3000','3')
    
    dir = 'Results/'
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


    plt.text(0.000002, 180 , r'$ m_{\tilde \chi_1 ^0}=$ ' + DM + ' TeV' , size=SIZE-5, ha="left", va="center" , color = 'red')
    plt.text(0.000002, 390 , r'$\tilde \chi_1 ^0  \tilde \chi_1 ^0 \rightarrow W^+ W^- Z $' , size=SIZE-5, ha="left", va="center" , color = 'red')
    plt.text(0.000002, 100 , label_CR , size=SIZE-5, ha="left", va="center", color = 'red')

    width = 1.2

    x = dic_EW['x']

    chans = ['WW']
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
    
    spec = Name_Dic[CR]
    
    
    FILES  = ['Data_n1ww_n1_' + DM_o + '_pythiaEW_False', 'Data_n1wwz_n1_' + DM_o + '_pythiaEW_False', 'Data_n1wwzz_n1_' + DM_o + '_pythiaEW_False']


    LABELS = [r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ $',
              r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ Z$' ,
              r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ ZZ$' ]
           
    COLORS = ['cyan' ,  'slateblue', 'blue' , 'navy']
    COLORS = ['cyan' , 'slateblue' , 'blue' ]
    XSEC_1 = []



    """ here i put the values of the crosss ection read in MG
    I have to rescale the values from pythia since they are normalized to unity
    So I keep a factor==1 for the LO sample
    and I multiply by the ratio of e.g. wwz/ww the wwz sample.
    """

    if DM_o == '1000':
       xsections_o = [96.5 , 12.4      , 0.6 ]
       xsections = [1    , 12.4/96.5 , 0.6/96.5 ]
    elif DM_o == '3000':
       xsections = []

    elif DM_o == '10000':
       xsections = []

    for C in chans:
        combi = []

        a = plt.plot(dic_noEW['x'] , dic_noEW[CR][DM_o+'.0'][C]   , color = 'black' , linestyle= '-' , linewidth = width , label = 'PPPC4DMID'    )
        b = plt.plot(dic_EW['x']   , dic_EW[CR][DM_o  +'.0'][C]   , color = 'black' , linestyle= '--', linewidth = width , label = 'PPPC4DMID EW' )

    
        handles.append( a[0] )
        handles.append( b[0] )

        first_legend = plt.legend(handles= handles, fontsize=SIZE-10, loc = 'upper right', fancybox=True , ncol = 1)
        frame = first_legend.get_frame()
        frame.set_edgecolor('gray')
        ax = plt.gca().add_artist(first_legend)

        handles = []
        # Samples with photons

        dic = {}
        for F,C,L,s,so in zip (FILES, COLORS, LABELS, xsections, xsections_o):


            F   = dir +'/' + F + '/' + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'
            x,y = READ(F)
            x = np.array([ math.pow(10,num) for num in x])/2 ### NB !!!! this factor 2 is because the EBEAM in pythia card was not 2*DM but only 1*DM !!! So x=Ekin/DM form pythia is actually 2*x
            
   	    if scaled:
		scale_tag = r'($\sigma=$ ' + str(so) + ') [pb]'
                y = np.array(y) * s
                dic[COLORS.index(C)] = y
   	    else:
		scale_tag = 'normalized to 1'

            a = plt.plot(x,y , color = C, linestyle = '-' , lw = width, label =  L + scale_tag )
            handles.append( a[0] )

        somma  = []
        for l,m,n in zip(dic[0], dic[1], dic[2]):
            s = l+m+n
            somma.append(s)

        c = plt.plot(x, somma, label = 'Total Spectrum', color = 'lime', ls = '--')	    
        handles.append(c[0])


    second_legend = plt.legend(handles= handles, fontsize=SIZE-10, loc = 'lower left', fancybox=True , ncol = 1)
    frame = second_legend.get_frame()
    frame.set_edgecolor('gray')
    ax = plt.gca().add_artist(second_legend)
    
    # plotting the Fermi sensitivity only for gamma rays
    if CR == 'gammas':
             Fermi_limits = [[ 0.5/float(DM) , 0.5/float(DM)],[-0.1, 70]]
             plt.plot(Fermi_limits[0],Fermi_limits[1] , color = 'gray', linestyle = '--')
             Fermi_limits = [[ 500/float(DM) , 500/float(DM)],[-2, 70]]
             plt.plot(Fermi_limits[0],Fermi_limits[1] , color = 'gray', linestyle = '--')
             place = 0.3
             if DM == '1': place = 10
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , place, 'Fermi Sensitivity'  , rotation=90, fontsize = 13 , color ='gray' )
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , 0.013, r'$\longrightarrow$' , fontsize = 20 , color ='gray' )

    plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
    os.system('mkdir PLOTS')
    os.system('mkdir PLOTS/n1ww_single/')

    plt.savefig('PLOTS/n1ww_single/' + DM + '_' + CR + '_n1ww_single_'+DM +'.pdf', bbox_inches='tight')
    plt.close()


# Load the Dictionary from the npy file  ### Tables[spectrum][mass][channel]
Dic_NoEW = np.load('../PPPC_Tables_noEW.npy', allow_pickle= True).item()
Dic_EW = np.load('../PPPC_Tables_EW.npy', allow_pickle= True).item()

#print Dic_NoEW['Particle_Spectra']

#['antiprotons', 'gammas', 'neutrinos_e', 'neutrinos_mu', 'neutrinos_tau', 'positrons']


DMs = ['1000']
CRs = ['gammas','positrons','neutrinos_e', 'neutrinos_tau' , 'neutrinos_mu' , 'antiprotons' ]
#CRs = ['gammas',]

for m in DMs:
    for c in CRs:
        print 'Producing the plot for the CR: ' + c + ' for a DM candidate of ' + m + ' GeV'
        Plot(m, dic_EW = Dic_EW, dic_noEW = Dic_NoEW , CR = c, scaled = True)






