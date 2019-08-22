""" Plots the contribution of tree, one emisison or two emission 
    of Z, photons and h bosons SEPARATELY """

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


from XSEC import * 

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
m_neu = r'$m_{\tilde \chi_1 ^0}$'
def xsection_plot(x1='', x2='', x3=''):
    SIZE = 15
    fig, ax = plt.subplots(1,1)
    plt.ylabel('Cross sections [pb]', fontsize = SIZE )
    #plt.xlabel('Process' , fontsize = SIZE )
    X = [1,2,3]
    plt.scatter(X, x1, label = m_neu + '= 1 TeV', color = 'blue' )
    plt.scatter(X, x2, label = m_neu + '= 3 TeV', color = 'cyan' )
    plt.scatter(X, x3, label = m_neu + '= 10 TeV', color = 'lime' )
    plt.xlim(0, 4)
    plt.ylim(0.1, 500)
    plt.yscale('log')
    xl = [r'$\tilde \chi_1 ^0  \tilde \chi_1 ^0  \rightarrow W^-W^+$'    ,
	  r'$\tilde \chi_1 ^0  \tilde \chi_1 ^0  \rightarrow W^-W^+ Z$'  ,
	  r'$\tilde \chi_1 ^0  \tilde \chi_1 ^0  \rightarrow W^-W^+ ZZ$' ]

    ax.set_xticks(X)
    ax.set_xticklabels(xl, minor = False, rotation= 30)
    plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
    plt.legend(loc= 'upper right' , fontsize = SIZE-3 )
    plt.savefig('PLOTS/n1ww_single/xsections_minimalDmwinolike.png', bbox_inches='tight')



""" Xsections extracted from the LHE files """
xsections_dic = { 'z' : { '1': { 'abs':  [96.5 , 12.4 , 0.6 ] , 'rel': [1 , 12.4/96.5  , 0.6/96.5    ] }  ,
	                  '3': { 'abs':  [18.63 , 5.51, 0.73] , 'rel': [1 , 5.51/18.63 , 0.73/18.63  ] }  ,
	                  '10': { 'abs':  [3.06, 1.71,   0.41] , 'rel': [1 , 1.71/3.06  , 0.411/3.06 ] } } , 



		  'a' : { '1': { 'abs':  [96.5 , 10.76 , 1.087 ] , 'rel': [1 , 12.4/96.5  , 0.6/96.5    ] }  , # ok
	                  '3': { 'abs':  [18.63 , 3.94, 0.32] , 'rel': [1 , 5.51/18.63 , 0.73/18.63  ] } , # ok
	                 '10': { 'abs':  [3.06, 1.08,   0.12] , 'rel': [1 , 1.71/3.06  , 0.411/3.06  ] } } , # missing aa


	          'h' : { '1': { 'abs':  [96.5 , 0.184 , 0.0007 ] , 'rel': [1 , 12.4/96.5  , 0.6/96.5    ] } ,
	                  '3': { 'abs':  [18.63 , 0.05, 0.0005] , 'rel': [1 , 5.51/18.63 , 0.73/18.63    ] } ,
	                 '10': { 'abs':  [3.06, 0.012,   0.0079] , 'rel': [1 , 1.71/3.06  , 0.411/3.06   ] } } ,  } # all ok



"""
   if DM_o == '1000':
       xsections_o = [96.5 , 12.4      , 0.6 ]
       xsections = [1    , 12.4/96.5 , 0.6/96.5 ]
    elif DM_o == '3000':
       xsections_o = [18.631 , 5.5153 , 0.731662023 ]
       xsections = [1 , 5.5153/18.63 , 0.7316/18.63 ]
    elif DM_o == '10000':
       xsections_o = [3.0623, 1.71248, 0.41186550998]
       xsections = [ 1, 1.71248/3.0623, 0.41186550998/3.0623 ]
"""

def Plot(DM, dic_EW = '', dic_noEW = '', CR = '', channel = '' , scaled = False, boson = 'z'):
    """ DM must be as the PPPC tables need it e.g. 1000.0 """


    DM_f = str(DM).replace('10000.0','10').replace('3000.0','3').replace('1000.0','1')

    
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
    
    
    FILES  = ['Data_n1n1_ww_' + DM_f + 'TeV', 'Data_n1n1_ww'+ boson +'_' + DM_f + 'TeV', 'Data_n1n1_ww'+ boson + boson +'_' + DM_f + 'TeV' ]



    if boson == 'z':
       l_boson = r'$Z$'
    elif boson =='h':
       l_boson = r'$h$'
    elif boson =='a':
       l_boson = r'$\gamma$'

    LABELS = [r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ $',
              r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ $' + l_boson ,
              r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ $' + l_boson + l_boson ]
           
    COLORS = ['cyan' ,  'slateblue', 'blue' , 'navy']
    COLORS = ['cyan' , 'slateblue' , 'blue' ]
    XSEC_1 = []



    """ here i put the values of the crosss ection read in MG
    I have to rescale the values from pythia since they are normalized to unity
    So I keep a factor==1 for the LO sample
    and I multiply by the ratio of e.g. wwz/ww the wwz sample.
    """

 
    xsections_abs , xsections_rel = xsections_dic[boson][DM_f]['abs'] , xsections_dic[boson][DM_f]['rel']
  
    for C in chans:
        combi = []
        DM = str(DM)
        a = plt.plot(dic_noEW['x'] , dic_noEW[CR][DM][C] , color = 'black' , linestyle= '-' , linewidth = width , label = 'PPPC4DMID'    )
        b = plt.plot(dic_EW['x']   , dic_EW[CR][DM][C]   , color = 'black' , linestyle= '--', linewidth = width , label = 'PPPC4DMID EW' )

    
        handles.append( a[0] )
        handles.append( b[0] )

        first_legend = plt.legend(handles= handles, fontsize=SIZE-10, loc = 'upper right', fancybox=True , ncol = 1)
        frame = first_legend.get_frame()
        frame.set_edgecolor('gray')
        ax = plt.gca().add_artist(first_legend)

        handles = []
        # Samples with photons

        dic = {}
        for F,C,L,s,so in zip (FILES, COLORS, LABELS, xsections_rel, xsections_abs):


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

    plt.savefig('PLOTS/n1ww_single/' + DM + '_' + CR + '_n1ww_single_'+DM + '_' + boson + '.pdf', bbox_inches='tight')
    plt.close()


# Load the Dictionary from the npy file  ### Tables[spectrum][mass][channel]
Dic_NoEW = np.load('../PPPC_Tables_noEW.npy', allow_pickle= True).item()
Dic_EW = np.load('../PPPC_Tables_EW.npy', allow_pickle= True).item()

#print Dic_NoEW['Particle_Spectra']

#['antiprotons', 'gammas', 'neutrinos_e', 'neutrinos_mu', 'neutrinos_tau', 'positrons']


DMs = ['1000.0' , '3000.0', '10000.0']
CRs = ['gammas','positrons','neutrinos_e', 'neutrinos_tau' , 'neutrinos_mu' , 'antiprotons' ]
#CRs = ['gammas',]


DMs = ['1000.0' , '3000.0' , '10000.0']
for m in DMs: 
  for h in ['h','z','a']:
    for c in CRs:
  
        print 'Producing the plot for the CR: ' + c + ' for a DM candidate of ' + m + ' GeV' + ' , boson' + h
        Plot(m, dic_EW = Dic_EW, dic_noEW = Dic_NoEW , CR = c, scaled = True, boson = h)






