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


from XSEC_and_plot import * 

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



def Plot(DM, dic_EW = '', dic_noEW = '', CR = '', channel = '' , scaled = False):
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


    plt.text(0.000002, 180 , r'$ m_{\tilde \chi_1 ^0}=$ ' + DM_f + ' TeV' , size=SIZE-5, ha="left", va="center" , color = 'red')
    plt.text(0.000002, 390 , r'$\tilde \chi_1 ^0  \tilde \chi_1 ^0 \rightarrow W^+ W^-  $' , size=SIZE-5, ha="left", va="center" , color = 'red')
    plt.text(0.000002, 100 , label_CR , size=SIZE-5, ha="left", va="center", color = 'red')

    width = 1.2

    x = dic_EW['x']

    chans = ['WW']

    handles = []
    
    spec = Name_Dic[CR]
    
    

    tree = r'$\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow W^-W^+ $'
           


  
    for C in chans:
        combi = []
        DM = str(DM)
        a = plt.plot(dic_noEW['x'] , dic_noEW[CR][DM][C] , color = 'lightgray' , linestyle= '-' , linewidth = width , label = 'PPPC4DMID'    )
        b = plt.plot(dic_EW['x']   , dic_EW[CR][DM][C]   , color = 'black' , linestyle= '-', linewidth = width , label = 'PPPC4DMID EW' )

    
        handles.append( a[0] )
        handles.append( b[0] )

        first_legend = plt.legend(handles= handles, fontsize=SIZE-12, loc = 'lower right', fancybox=True , ncol = 1)
        frame = first_legend.get_frame()
        frame.set_edgecolor('gray')
        ax = plt.gca().add_artist(first_legend)


 	de, y   = READ('Results/Data_n1n1_ww_'+DM_f+'TeV/'  + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat')
 	de, y_z = READ('Results/Data_n1n1_wwz_'+DM_f+'TeV/' + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat')
  	de, y_h = READ('Results/Data_n1n1_wwh_'+DM_f+'TeV/' + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat')
   	de, y_a = READ('Results/Data_n1n1_wwa_'+DM_f+'TeV/' + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat')
        x = np.array([ math.pow(10,num) for num in de]) 
        handles = [] 
        somma = []
    	for y, ya, yz, yh  in zip (y, y_a, y_z, y_h):
            s = y * xsections_dic['a'][DM_f]['rel'][0]  + yz * xsections_dic['z'][DM_f]['rel'][1] + ya * xsections_dic['a'][DM_f]['rel'][1] + yh * xsections_dic['h'][DM_f]['rel'][1]
            somma.append(s) 
        xsec = xsections_dic['a'][DM_f]['abs'][0] + xsections_dic['z'][DM_f]['abs'][1] +  xsections_dic['a'][DM_f]['abs'][1] +  xsections_dic['h'][DM_f]['abs'][1] 
 	g = plt.plot(x, somma, label = r'Sum $(tree+ \gamma +z+h)$[' + str(xsec) + 'pb]', color = 'magenta', ls = '-')	    
   	handles.append(g[0])



        # Samples with photons
   
        dic = {}

        #    'Data_n1n1_ww_' + DM_f + 'TeV'

        FILES = [ 'Data_n1n1_ww_'  + DM_f  + 'TeV' ,
		  'Data_n1n1_wwa_' + DM_f + 'TeV' ,
	          'Data_n1n1_wwh_' + DM_f + 'TeV' , 
	          'Data_n1n1_wwz_' + DM_f + 'TeV' , 
		  'Data_n1n1_wwx_' + DM_f + 'TeV' , 
		  'Data_n1n1_wwwwx_' + DM_f + 'TeV' , 
]

        COLORS = ['blue', 'yellow', 'red', 'cyan', 'orange', 'lime']

        COLORS = ['slateblue', 'cyan', 'lime', 'yellow', 'orange', 'blue']

        xsections_abs = [ xsections_dic['z'][DM_f]['abs'][0], xsections_dic['a'][DM_f]['abs'][1], xsections_dic['h'][DM_f]['abs'][1], xsections_dic['z'][DM_f]['abs'][1], xsections_dic['x'][DM_f]['abs'][1],
			  float(xsections_dic['all'][DM_f]['abs'][1])     ]

        xsections_rel = [ xsections_dic['z'][DM_f]['rel'][0], xsections_dic['a'][DM_f]['rel'][1], xsections_dic['h'][DM_f]['rel'][1], xsections_dic['z'][DM_f]['rel'][1] ,xsections_dic['x'][DM_f]['rel'][1],
			  float(xsections_dic['all'][DM_f]['abs'][1])/ xsections_dic['all'][DM_f]['abs'][0]   ]




        LABELS = [ tree , tree + r'$\gamma$' , tree + r'$h$' , tree + r'$z$' , tree + r'$x$' , tree + '+' r'$W^-W^- X$' ]

        for F,C,L,s,so in zip (FILES, COLORS, LABELS, xsections_rel, xsections_abs):


            F   = dir +'/' + F + '/' + Name_Dic[CR] + '_test1000GeV_ww_lhe.dat'
            x,y = READ(F)
            x = np.array([ math.pow(10,num) for num in x]) 
            
   	    if scaled:
		scale_tag = r' [' + str(so) + 'pb]'
                y = np.array(y) * s
                dic[COLORS.index(C)] = y
   	    else:
		scale_tag = 'normalized to 1'

            a = plt.plot(x,y , color = C, linestyle = '--' , lw = width, label =  L + scale_tag )
            handles.append( a[0] )

        



        

        

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
             place = 0.3
             if DM == '1': place = 10
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , place, 'Fermi Sensitivity'  , rotation=90, fontsize = 11 , color ='gray' )
             plt.text( 0.5/float(DM) + 0.5/float(DM)/5 , 0.013, r'$\longrightarrow$' , fontsize = 20 , color ='gray' )

    plt.grid(which='major', linestyle=':', color = 'lightgray', lw = 1.05)
    os.system('mkdir PLOTS')
    os.system('mkdir PLOTS/n1ww_comparison/')

    plt.savefig('PLOTS/n1ww_comparison/' + DM + '_' + CR + '_n1ww_comparison_'+DM + '.pdf', bbox_inches='tight')
    plt.close()


# Load the Dictionary from the npy file  ### Tables[spectrum][mass][channel]
Dic_NoEW = np.load('../PPPC_Tables_noEW.npy', allow_pickle= True).item()
Dic_EW = np.load('../PPPC_Tables_EW.npy', allow_pickle= True).item()

#print Dic_NoEW['Particle_Spectra']

#['antiprotons', 'gammas', 'neutrinos_e', 'neutrinos_mu', 'neutrinos_tau', 'positrons']


DMs = ['1000.0' , '3000.0', '10000.0']
CRs = ['gammas','positrons','neutrinos_e', 'neutrinos_tau' , 'neutrinos_mu' , 'antiprotons' ]
#CRs = ['gammas',]



for m in DMs:

    for c in CRs:
  
        print 'Producing the plot for the CR: ' + c + ' for a DM candidate of ' + m + ' GeV' 
        Plot(m, dic_EW = Dic_EW, dic_noEW = Dic_NoEW , CR = c, scaled = True)






