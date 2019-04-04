import os,sys
import matplotlib
from matplotlib  import cm
from matplotlib import ticker
import matplotlib.pyplot as plt
import pickle
import os.path
import numpy as np
import matplotlib.image as image
import numpy
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.cbook import get_sample_data

#matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.unicode'] = True
#plt.rcParams['text.latex.preamble'] = [
#                                       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
#                                       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
#                                       r'\usepackage{helvet}',    # set the normal font here
#                                       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
#                                       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
#                                      ]


'''
    Reading masses and limits from Fermi file (to draw the validation line)
'''
def Read_Fermi_File(input_file='',dwarf = ''):
    
    num = 0
    if   dwarf == 'bootes_I'          : num = 1
    elif dwarf == 'bootes_II'         : num = 2
    elif dwarf == 'bootes_III'        : num = 3
    elif dwarf == 'canes_venatici_I'  : num = 4
    elif dwarf == 'canes_venatici_II' : num = 5
    #    elif dwarf == 'canis_major'       : num =  # no such dwarf in the file
    elif dwarf == 'carina'            : num = 6
    elif dwarf == 'coma_berenices'    : num = 9
    elif dwarf == 'draco'             : num = 10
    elif dwarf == 'fornax'            : num = 14
    elif dwarf == 'hercules'          : num = 17
    elif dwarf == 'leo_I'             : num = 23
    elif dwarf == 'leo_II'            : num = 24
    elif dwarf == 'leo_IV'            : num = 25
    elif dwarf == 'leo_V'             : num = 26
    elif dwarf == 'pisces_II'         : num = 30
    elif dwarf == 'reticulum_II'      : num = 31
    #    elif dwarf == 'sagittarius'       : num = # no such dwarf in the file
    elif dwarf == 'sculptor'          : num = 34
    elif dwarf == 'segue_1'           : num = 35
    # elif dwarf == 'segue_2'           : num = # no such dwarf in the file
    elif dwarf == 'sextans'           : num = 36
    elif dwarf == 'ursa_major_I'      : num = 42
    elif dwarf == 'ursa_major_II'     : num = 43
    elif dwarf == 'ursa_minor'        : num = 44
    elif dwarf == 'willman_1'         : num = 45
    elif dwarf == 'tot'               : num = 46
    else:
         print 'This dwarf does not exists! check!'
         sys.exit()
    data   = np.loadtxt(input_file,unpack=True)
    mass   = data[0]
    lim    = data[num]
    return mass , lim

color_T , color_B = 'navy', 'cornflowerblue'


def Apply_Plot_Properties(pretty_dwarf='Total' , vers = ''):
    
      global color_T , color_B
      
      pos_1, pos_2, pos_3 = 3 , 10**(-22) , 3*10**(-23)
      if vers == 'Global':
         pos_1, pos_2, pos_3 = 110 , 2.1*10**(-23) , 5.4*10**(-23)
      
      SIZE = 21
      THICK_LABEL_SIZE = 15
      plt.text(3,   4*10**(-22),  pretty_dwarf      , size=SIZE, ha="left", va="center", color = 'black', ) #bbox=dict(facecolor='none', edgecolor='none')
      plt.text(pos_1,   pos_2,  r'$ \chi \chi \rightarrow \tau ^+ \tau ^-$', size=SIZE, ha="left", va="center", color = color_T, ) #bbox=dict(facecolor='none', edgecolor='none')
      plt.text(pos_1,   pos_3,  r'$ \chi \chi \rightarrow b \bar b  $', size=SIZE, ha="left", va="center", color = color_B, ) #bbox=dict(facecolor='none', edgecolor='none')
      
      

      plt.ylabel(r'$< \sigma v >$ [cm$^3$ s$^{-1}$]'     , fontsize = SIZE)
      plt.xlabel(r'$m_{\chi}$ [GeV]'                  , fontsize = SIZE)
      plt.xlim(2,10000 )
      plt.ylim(5*10**(-28), 10**(-21))
      plt.yscale('log')
      plt.xscale('log')
  
      plt.tick_params(axis='both', which='major', labelsize=THICK_LABEL_SIZE, length=8, top='off', right='off')
      plt.tick_params(axis='both', which='minor', labelsize=THICK_LABEL_SIZE, length=5, top='off', right='off')


Pretty  = {'ursa_major_II'     : r'Ursa Major II $    (  J \ = \ 10^{19.4})$' ,
           'ursa_minor'        : r'Ursa Minor $       (  J \ = \ 10^{18.9})$' ,
           'willman_1'         : r'Willman I $        (  J \ = \ 10^{18.9})$'  ,
           'sextans'           : r'Sextans $          (  J \ = \ 10^{17.5})$'  ,
           'segue_1'           : r'Segue 1 $          (  J \ = \ 10^{19.4})$' ,
           'sculptor'          : r'Sculptor $         (  J \ = \ 10^{18.5})$'  ,
           'leo_II'            : r'Leo II $           (  J \ = \ 10^{18.0})$'  ,
           'leo_IV'            : r'Leo IV $           (  J \ = \ 10^{16.3})$'  ,
           'hercules'          : r'Hercules $         (  J \ = \ 10^{16.9})$'  ,
           'fornax'            : r'Fornax $           (  J \ = \ 10^{17.8})$'  ,
           'draco'             : r'Draco $            (  J \ = \ 10^{18.8})$' ,
           'coma_berenices'    : r'Coma Berenices $   (  J \ = \ 10^{19.0})$' ,
           'carina'            : r'Carina $           (  J \ = \ 10^{17.9})$'  ,
           'canes_venatici_II' : r'Canes Venatici II $(  J \ = \ 10^{17.6})$'  ,
           'bootes_I'          : r'Bootes I$          (  J \ = \ 10^{18.2})$'  ,
           'reticulum_II'      : r'Reticulum II$      (  J \ = \ 10^{18.9})$'  ,



}

#    This script produces the Fermi bounds for each single dwarf , in the "mumu" and "bb" channels,
#    and compares with the official limit from Fermi.
#    Dic is the dictionary containing the bb and tautau limits for each dwarf :
#        Single_Dwarf_Limits_WithMarginalaisation_From5GeV.npy
#    Dwarves_List = ['bootes_I', 'coma_berenices', 'draco', 'fornax', 'sculptor', 'segue_1', 'ursa_major_II', 'ursa_minor', 'reticulum_II' ]

def Validate_SingleDwarf(flag = '' , lista = ''):
    
    global color_T , color_B

    RES        = np.load('Numpys/Single_Dwarf.npy').item()
    RES_two  = np.load('Numpys/SingleDwarfs_Limits_Twosided.npy').item()
    
    
    
    for DWARF in lista:
        
      print 'I am doing the Dwarf: ' , DWARF
      bb , tautau       = RES[DWARF]['bb'] , RES[DWARF]['tautau']
      bb_2 , tautau_2 = RES_two[DWARF]['bb'] , RES_two[DWARF]['tautau']



    
      pretty = Pretty[DWARF]
      Apply_Plot_Properties(pretty_dwarf= pretty)
      
      # bb channel ( I have to remove the value for mDM = 5 since the limits is wrong )
      plot = plt.plot(Masses[1:], bb[1:]        , linewidth = 1.3 , linestyle = '-' , color = color_B )
      plot = plt.plot(Masses[1:], bb_2[1:] , linewidth = 1.3 , linestyle = ':' , color = color_B )

      mass_f , lim_f = Read_Fermi_File(input_file='Fermi-Data/likelihoods/limits_bb.txt',dwarf = DWARF)
      plt.plot(mass_f , lim_f , color = color_B  , linestyle='--')
    




      # tautau channel
      plot = plt.plot(Masses, tautau        , linewidth = 1.3 , linestyle = '-' , color = color_T )
      plot = plt.plot(Masses, tautau_2 , linewidth = 1.3 , linestyle = ':' , color = color_T )
    
      mass_f , lim_f = Read_Fermi_File(input_file='Fermi-Data/likelihoods/limits_tautau.txt',dwarf = DWARF)
      plt.plot(mass_f , lim_f , color = color_T  , linestyle='--')

      # legend
      plt.plot([-5],[-5], label = 'MadDM oneortwosided=1'  , color = 'gray',  linewidth = 1.3 , linestyle = '-' )
      plt.plot([-5],[-5], label = 'MadDM oneortwosided=2'  , color = 'gray',  linewidth = 1.3 , linestyle = ':' )
      plt.plot([-5],[-5], label = 'Fermi-LAT(2016)'        , color = 'gray',  linewidth = 1.3 , linestyle = '--' )

      legend = plt.legend(fontsize=12, loc = 'lower right', fancybox = True )
      frame = legend.get_frame()
      frame.set_edgecolor('gray')

      os.system('mkdir PLOTS')
      os.system('mkdir PLOTS/Dwarves/')
      plt.savefig('PLOTS/HQ_'+flag+'_'+DWARF+'_Validation.png', bbox_inches='tight', dpi = 250 )
      plt.savefig('PLOTS/'+flag+'_'+DWARF+'_Validation.png', bbox_inches='tight', dpi = 160 )

      plt.close()



def Validate_Combined_Fermions(flag = ''):

      color_qq , color_cc , color_tt , color_ee , color_mumu  = 'cyan' , 'blue', 'forestgreen', 'red', 'orange'
      
      SIZE = 17
      THICK_LABEL_SIZE = 15
      plt.text(3,   4*10**(-22),  'Fermi Limits - Combined (Fermions)'      , size=SIZE, ha="left", va="center", color = 'black', ) #bbox=dict(facecolor='none', edgecolor='none')

      #plt.text(pos_1,   pos_2,  r'$ \chi \chi \rightarrow \tau ^+ \tau ^-$', size=SIZE, ha="left", va="center", color = color_T, ) #bbox=dict(facecolor='none', edgecolor='none')
      #plt.text(pos_1,   pos_3,  r'$ \chi \chi \rightarrow b \bar b  $', size=SIZE, ha="left", va="center", color = color_B, ) #bbox=dict(facecolor='none', edgecolor='none')
      
      plt.ylabel(r'$< \sigma v >$[cm$^3$ s$^{-1}$]'  , fontsize = SIZE)
      plt.xlabel(r'$m_{\chi}$ [GeV] '            , fontsize = SIZE)
      plt.xlim(2,100000 )
      plt.ylim(5*10**(-28), 10**(-21))
      plt.yscale('log')
      plt.xscale('log')
      Width = 1.7
      plt.tick_params(axis='both', which='major', labelsize=THICK_LABEL_SIZE, length=8, top='off', right='off')
      plt.tick_params(axis='both', which='minor', labelsize=THICK_LABEL_SIZE, length=5, top='off', right='off')

      RES = np.load('Combined_Limits.npy').item()
      LOW = np.load('Combined_Limits_p8lowmass.npy').item()

      Masses_Low = [2,3,4] + Masses
          
          #LOW_tautau = LOW['Combined']['tautau'] + RES['Combined']['tautau']
      LOW_mumu   = LOW['Combined']['mumu']   + RES['Combined']['mumu']
      LOW_ee     = LOW['Combined']['ee']     + RES['Combined']['ee']
      LOW_qq     = LOW['Combined']['qq']     + RES['Combined']['qq']
      LOW_cc     = LOW['Combined']['cc']     + RES['Combined']['cc']

      # adding new cc , ee , mumu
      new_cc      = np.load('Pythia8_cc_gluglu.npy').item()['Combined']['cc']
      LOW_cc_new  = LOW['Combined']['cc'] + new_cc

      new_ee      = np.load('Pythia8_ee_mumu.npy').item()['Combined']['ee']
      LOW_ee_new  = LOW['Combined']['ee'] + new_ee

      new_mumu    = np.load('Pythia8_ee_mumu.npy').item()['Combined']['mumu']
      LOW_mumu_new  = LOW['Combined']['mumu'] + new_mumu
      # to CHECK spectra low masses attachment
      #plot = plt.plot(Masses_Low,LOW_ee_new  , color = 'gray'    , label = 'ee all Py8')
      #plot = plt.plot(Masses_Low,LOW_mumu_new, color = 'gray'    , label = 'mumu all Py8')


      
    
      plot = plt.plot(Masses_Low, LOW_qq  , linewidth = Width-0.6 , linestyle = '-' , color = color_qq  , label = r'$ \chi \chi \rightarrow u \bar u$' )
      #plot = plt.plot(Masses_Low, LOW_cc  , linewidth = Width+1 , linestyle = ':'   , color = color_cc  , label = r'$ \chi \chi \rightarrow c \bar c$' )
      plot = plt.plot(Masses_Low,LOW_cc_new, linewidth = Width+1 , linestyle = ':'   , color = color_cc  , label = r'$ \chi \chi \rightarrow c \bar c$' )

      #plot = plt.plot(Masses[1:], RES['Combined']['bb'][1:]   , linewidth = Width , linestyle = '-'  , color = color_bb  , label = r'$ \chi \chi \rightarrow b \bar b$' )

      M_tt , Lim_tt = [],[]
      for m, l in zip(Masses, RES['Combined']['tt']):
          if m > 175:
             M_tt.append(m), Lim_tt.append(l)
      plot = plt.plot(M_tt, Lim_tt    , linewidth = Width , linestyle = '--' , color = color_tt  , label = r'$ \chi \chi \rightarrow t \bar t$' )


      plot = plt.plot(Masses_Low, LOW_ee         , linewidth = Width , linestyle = '--'  , color = color_ee     , label = r'$ \chi \chi \rightarrow e^+ e^- $' )
      plot = plt.plot(Masses_Low, LOW_mumu       , linewidth = Width , linestyle = ':'   , color = color_mumu   , label = r'$ \chi \chi \rightarrow \mu ^+ \mu ^- $' )
#      plot = plt.plot(Masses_Low, LOW_tautau     , linewidth = Width , linestyle = '-'   , color = color_tautau , label = r'$ \chi \chi \rightarrow \tau ^+ \tau ^- $' )
      
#RES_low = np.load('Limits_LowMasses_Py8.npy').item()

#plot = plt.plot(RES_low['Masses'], RES_low['uu']  , linewidth = 1.4   , linestyle = '-' , color = color_qq )
#plot = plt.plot(RES_low['Masses'], RES_low['cc']  , linewidth = 1.4   , linestyle = '-' , color = color_cc )
#plot = plt.plot(RES_low['Masses'], RES_low['ee']  , linewidth = 1.4   , linestyle = '-' , color = color_ee )
#plot = plt.plot(RES_low['Masses'], RES_low['mumu'], linewidth = 1.4   , linestyle = '-' , color = color_mumu )

      plt.grid()
      '''
      ax = plt.gca()
      xy = [3.0, 5*10**(-24)]

      arr_img = plt.imread('Dwarves_J.png')

      imagebox = OffsetImage(arr_img, zoom=1.3)
      imagebox.image.axes = ax

      ab = AnnotationBbox(imagebox, xy, xybox=(75, 1.7*10**(-23)), xycoords='data', boxcoords="offset points", pad=0 )

      ax.add_artist(ab)
      '''
      legend = plt.legend(fontsize=15, loc = 'lower right', fancybox = True ,ncol = 2)
      frame = legend.get_frame()
      frame.set_edgecolor('gray')

      os.system('mkdir PLOTS')
      os.system('mkdir PLOTS/Dwarves/')
      plt.savefig('PLOTS/NewLim_'+flag+'.png', bbox_inches='tight', dpi = 160 )
      plt.savefig('PLOTS/HQ_NewLim_'+flag+'.png', bbox_inches='tight', dpi = 250 )

      plt.close()


def Validate_Combined_Bosons(flag = ''):
    
      SIZE = 17
      THICK_LABEL_SIZE = 15
      plt.text(3,   4*10**(-22),  'Fermi Limits - Combined (Bosons)'      , size=SIZE, ha="left", va="center", color = 'black', ) #bbox=dict(facecolor='none', edgecolor='none')

      #plt.text(pos_1,   pos_2,  r'$ \chi \chi \rightarrow \tau ^+ \tau ^-$', size=SIZE, ha="left", va="center", color = color_T, ) #bbox=dict(facecolor='none', edgecolor='none')
      #plt.text(pos_1,   pos_3,  r'$ \chi \chi \rightarrow b \bar b  $', size=SIZE, ha="left", va="center", color = color_B, ) #bbox=dict(facecolor='none', edgecolor='none')
      
      plt.ylabel(r'$< \sigma v >$[cm$^3$ s$^{-1}$]'  , fontsize = SIZE)
      plt.xlabel(r'$m_{\chi}$ [GeV] '            , fontsize = SIZE)
      plt.xlim(2,100000 )
      plt.ylim(5*10**(-28), 10**(-21))
      plt.yscale('log')
      plt.xscale('log')
  
      plt.tick_params(axis='both', which='major', labelsize=THICK_LABEL_SIZE, length=8, top='off', right='off')
      plt.tick_params(axis='both', which='minor', labelsize=THICK_LABEL_SIZE, length=5, top='off', right='off')

      plt.grid()
      RES = np.load('Combined_Limits.npy').item()
      print RES
      
      
      LOW = np.load('Combined_Limits_p8lowmass.npy').item()
      Masses_Low = [2,3,4] + Masses
      
      new_gg     = np.load('Pythia8_cc_gluglu.npy').item()['Combined']['gg']
      LOW_gg_new  = LOW['Combined']['gg'] + new_gg


      M_ww , Lim_ww = [],[]
      for m, l in zip(Masses, RES['Combined']['WW']):
          if m > 80:
              M_ww.append(m), Lim_ww.append(l)

      M_zz , Lim_zz = [],[]
      for m, l in zip(Masses, RES['Combined']['ZZ']):
          if m > 90:
              M_zz.append(m), Lim_zz.append(l)

      M_hh , Lim_hh = [],[]
      for m, l in zip(Masses, RES['Combined']['hh']):
          if m > 125:
              M_hh.append(m), Lim_hh.append(l)



      plot = plt.plot(M_ww, Lim_ww            , linewidth = 1.3 , linestyle = '-'  , color = 'gold'  , label = r'$ \chi \chi \rightarrow W ^+ W ^- $' )
      plot = plt.plot(M_zz, Lim_zz            , linewidth = 2.3 , linestyle = '-.' , color = 'blue'  , label = r'$ \chi \chi \rightarrow Z  Z$' )
      plot = plt.plot(M_hh, Lim_hh            , linewidth = 1.3 , linestyle = '--' , color = 'limegreen'  , label = r'$ \chi \chi \rightarrow h  h $' )
      plot = plt.plot(Masses_Low, LOW_gg_new  , linewidth = 2.3 , linestyle = ':'  , color = 'red'  , label = r'$ \chi \chi \rightarrow g g $' )
      #plot = plt.plot(Masses_Low, LOW_gg_new    , linewidth = 1.4 , linestyle = '-' , color = 'gray'  , label = 'new gg' )


      legend = plt.legend(fontsize=15, loc = 'lower right', fancybox = True )
      frame = legend.get_frame()
      frame.set_edgecolor('gray')

      os.system('mkdir PLOTS')
      os.system('mkdir PLOTS/Dwarves/')
      plt.savefig('PLOTS/NewLim_'+flag+'.png', bbox_inches='tight', dpi = 160 )
      plt.savefig('PLOTS/HQ_NewLim_'+flag+'.png', bbox_inches='tight', dpi = 250 )

      plt.close()


'''
def Plot_Spectra_5GeV(flag = ''):

    folder = 'Pythia8_LowMasses'
    Channels_P8 = ['CC' , 'EE', 'MUMU','TAUTAU','GLUONGLUON' , 'UU' ]
    Channels_CP = ['cc' , 'ee', 'mumu','tautau','gg'         , 'qq']
    colors      = ['blue' , 'lime', 'red', 'gold', 'black', 'magenta']
    
    TAB = np.load('/Users/Federico/Dropbox/LLN/Create_PPPC_Python_Tables/PPPC_Tables_noEW.npy').item()

    for C, CP , col in zip(Channels_P8, Channels_CP, colors):
        
        F_name = folder+'/gamma_x_5_'+C+'.dat'
        x , y = np.loadtxt(F_name, unpack = True)

        yt = TAB['gammas']['5.0'][CP]

        plt.text (-8.5 , 0.01, '-- : Pythia8')
        plt.text (-8.5 , 0.017, '-  : PPPPC4DMID')

        plt.plot(x  , y  , linestyle = '--'  , color = col , linewidth = 1.4)
        plt.plot(x  , yt , color = col , label = r'$\chi \chi \rightarrow $ ' + CP , linewidth = 1.4 )
    
    plt.xlabel('logx')
    plt.ylabel('dn/logx')
    
    plt.title('Spectra Comparison at DM = 5 GeV (500k events)')
    plt.yscale('log')
#plt.xscale('log')
    
    plt.legend(fontsize = 10 , loc = 'best')
    plt.savefig('PLOTS/Verify_5GeV_Spectra.png' , dpi = 300)
'''

Masses  = [5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1300.0, 1500.0, 1700.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0, 12000.0, 15000.0, 20000.0, 30000.0, 50000.0, 100000.0]






Dwarves_List = ['draco', 'segue_1', 'ursa_major_II', 'ursa_minor', 'reticulum_II' ,'coma_berenices' ]

Validate_SingleDwarf(flag = '' , lista = Dwarves_List)





