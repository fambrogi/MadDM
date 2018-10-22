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

os.system('mkdir PLOTS')
def Apply_Plot_Properties(vers = 'no', C = ''):
    
      global color_T , color_B
      
      pos_1, pos_2 = 3 , 10**(-22)

      SIZE = 21
      THICK_LABEL_SIZE = 15
      if C == 'tautau': plt.text(pos_1, pos_2,  r'$ \chi \chi \rightarrow \tau ^+ \tau ^-$', size=SIZE, ha="left", va="center", color = 'black') #bbox=dict(facecolor='none', edgecolor='none')
      if C == 'bb' : plt.text(pos_1, pos_2,  r'$ \chi \chi \rightarrow b \bar b  $', size=SIZE, ha="left", va="center", color = 'black') #bbox=dict(facecolor='none', edgecolor='none')
      
      plt.text(pos_1, 5*10**(-22), r'Limits Comparison - MadDM Only', size=SIZE-5, ha="left", va="center", color = 'black')

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




def Validate_All_One(flag = '' , Channels = ''):
    
    global color_T , color_B

    RES        = np.load('Numpys/Single_Dwarf.npy').item()
    
    Dwarfs_List = {'draco'          : { 'C' : 'blue'     , 'S' : '-' },
                   'segue_1'        : { 'C' : 'slateblue'     , 'S' : '-' },
                   'ursa_major_II'  : { 'C' : 'dodgerblue'     , 'S' : '-' },
                   'ursa_minor'     : { 'C' : 'cyan'     , 'S' : '-' },
                   'reticulum_II'   : { 'C' : 'navy'  , 'S' : '-' },
                   'coma_berenices' : { 'C'  : 'purple'   , 'S' : '-' } }
    
    Tab_6 = numpy.load('Numpys/Combined_Limits-Onlybbtautau.npy').item()
    Tab_6_NoProf = numpy.load('Numpys/Combined_Limits-Onlybbtautau_NoMarg.npy').item()


    for C in Channels:
      
      for DWARF in Dwarfs_List.keys():
 
           lim = RES[DWARF][C]

           pretty = Pretty[DWARF]
           Apply_Plot_Properties(C = C)
      
           plot = plt.plot(Masses[1:], lim[1:] , linewidth = 1.1 , linestyle = Dwarfs_List[DWARF]['S'] , color = Dwarfs_List[DWARF]['C'] , label = DWARF  )

      MADDM_6        = Tab_6['Combined'][C]
      MADDM_6_NoProf = Tab_6_NoProf['Combined'][C]

      if C == 'tautau':
          plt.plot(Masses     , MADDM_6            , color = 'red'  , linestyle='-'   , label = 'MadDM'          , linewidth = 1.5 )
          plt.plot(Masses     , MADDM_6_NoProf     , color = 'lime' , linestyle='--'  , label = 'MadDM ' , linewidth = 1.5 )

      if C == 'bb':
          plt.plot(Masses[1:] , MADDM_6[1:]        , color = 'red'  , linestyle='-'   , label = 'MadDM' , linewidth = 1.5 )
          plt.plot(Masses[1:] , MADDM_6_NoProf[1:] , color = 'lime' , linestyle='--'  , label = 'MadDM No Prof.' , linewidth = 1.5 )


      mass_f , lim_f = Read_Fermi_File(input_file='likelihoods/limits_'+C+'.txt', dwarf = 'tot' )
      plt.plot(mass_f , lim_f , color = 'lightgray' , linestyle='-' , label = 'Fermi-LAT 2016', linewidth = 1.5 )


      plt.grid()
      legend = plt.legend(fontsize=9, loc = 'lower right', fancybox = True , ncol = 2)
      frame = legend.get_frame()
      frame.set_edgecolor('gray')

      plt.savefig('PLOTS/All_Validation_MadDM_' + C + '.png', bbox_inches='tight', dpi = 250 )

      plt.close()



Masses  = [5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1300.0, 1500.0, 1700.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0, 12000.0, 15000.0, 20000.0, 30000.0, 50000.0, 100000.0]


Channels = ['tautau','bb']

Validate_All_One(flag = '', Channels = Channels )



