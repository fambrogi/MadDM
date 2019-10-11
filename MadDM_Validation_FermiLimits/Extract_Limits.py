"""
Module for extracting the Fermi-LAT limits using a set of spectra.
The calculation is identical to what used in MadDM 3.0 .

Author:: Ambrogi Federico, federico.ambrogi88@gmail.com

"""


import os,sys
import matplotlib
from matplotlib  import cm
from matplotlib import ticker
import matplotlib.pyplot as plt
import pickle
import os.path
from fermi_limits_JmodFeb8_Twosided import *



Masses  = [5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1300.0, 1500.0, 1700.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0, 12000.0, 15000.0, 20000.0, 30000.0, 50000.0, 100000.0]


# Extracting the Fermi-LAT UL lines for the dwarf selected. See list below

def Read_Fermi_File(input_file='' , dwarf=''):
    
    num = 0
    if   dwarf == 'bootes_I'          : num = 1
    elif dwarf == 'bootes_II'         : num = 2
    elif dwarf == 'bootes_III'        : num = 3
    elif dwarf == 'canes_venatici_I'  : num = 4
    elif dwarf == 'canes_venatici_II' : num = 5
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
    elif dwarf == 'sculptor'          : num = 34
    elif dwarf == 'segue_1'           : num = 35
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


'''
    This script calculates the bb and tautau limits , to be used for validation of a single dwarf
    The results are saved in a numpy file called Single_Dwarf_Limits_WithMarginalisation_From5GeV
    
    Input parameters:
        - list of dSph to be combined
        - Masses of the DM candidates
        - PPPC tables loaded from the dictionary
        - name of the .npy file that is being saved
'''

def Extract_Limits_SingleDwarf(Dwarves_List = '' , Masses = '' , Tables =  '' , saveAs='Check'):
  print '*** Extracting Individual dSphs Fermi_LAT limits for the bb and tautau Channels ***'

  single_dwarf_limits = {}
  single_dwarf_limits['Masses'] = Masses
  for D in Dwarves_List:
    print 'Doing the dwarf', D
    dwarf = D
    single_dwarf_limits[dwarf] = {}
    single_dwarf_limits[dwarf]['tautau'] = []
    single_dwarf_limits[dwarf]['bb'] = []
    
    lista = [D]
    dic = dw_dic(dwarf_list = lista)

    for mDM in Masses: # Filling the lists with the limits for each DM mass
        mDM = str(mDM)
        x , bb, tautau = Tables['x'] , Tables['gammas'][mDM]['bb'] , Tables['gammas'][mDM]['tautau']
        bb_lim =      Fermi_sigmav_lim(mDM, x = x , dndlogx = bb      , dw_in = dic , marginalize = False)[0]
        tautau_lim =  Fermi_sigmav_lim(mDM, x = x , dndlogx = tautau  , dw_in = dic , marginalize = False)[0]
        single_dwarf_limits[dwarf]['bb'].     append( bb_lim  )
        single_dwarf_limits[dwarf]['tautau']. append( tautau_lim  )
        print 'DM , bb , tautau ' , mDM , ' ' , bb_lim , ' ' , tautau_lim
  np.save('SingleDwarfs_'+saveAs, single_dwarf_limits)
  print 'Done saving the numpy dictionary ' , 'SingleDwarfs_'+saveAs


'''
    See description above.
    In addition, the field Channels =   can be used to select the annihilation Channels of interest
    # Channels = ['ee', 'mumu', 'tautau', 'qq', 'cc','bb', 'tt', 'ZZ', 'WW', 'hh', 'gammagamma', 'gg'] as in the PPPC tables
'''

def Extract_Limits_Combined(Dwarves_List = '' , Masses = '' , Tables =  '' , Channels = '' , saveAs='Check'):
  print '*** Extracting Combined Fermi_LAT limits ***'
  print 'List of Dwarfs: **** \n' , Dwarves_List
  print 'List of Channels: **** \n' , Channels

  combined_limits             = {}
  combined_limits['Combined'] = {}

  Channels = ['tautau', 'bb' ]
  
  dic = dw_dic(dwarf_list = Dwarves_List)

  for C in Channels:
    combined_limits['Combined'][C] = []
    for mDM in Masses: # Filling the lists with the limits for each DM mass
        mDM = str(mDM)
        x = Tables['x']
        print C
        y = Tables['gammas'][mDM][C]
        lim = Fermi_sigmav_lim(mDM, x = x , dndlogx = y      , dw_in = dic , marginalize = False)[0]
        combined_limits['Combined'][C]. append( lim  )
        print 'mDM, lim ', mDM , ' ' , lim
  np.save('Combined_' + saveAs, combined_limits)
  print 'Done saving the numpy dictionary ' , 'Combined_'+saveAs


print 'Loading the PPPC Tables **** \n'
Tables    = np.load('Numpys/PPPC_Tables_noEW.npy', allow_pickle=True).item()

Masses  = [5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1300.0, 1500.0, 1700.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0, 12000.0, 15000.0, 20000.0, 30000.0, 50000.0, 100000.0]

Dwarves_List = ['draco', 'coma_berenices', 'segue_1', 'ursa_major_II', 'ursa_minor', 'reticulum_II' ]

Channels = ['ee', 'mumu', 'tautau', 'qq', 'cc','bb', 'tt', 'ZZ', 'WW', 'hh', 'gammagamma', 'gg']

Extract_Limits_SingleDwarf(Dwarves_List = Dwarves_List , Masses = Masses , Tables =  Tables , saveAs = 'EW')
Extract_Limits_Combined   (Dwarves_List = Dwarves_List , Masses = Masses , Tables =  Tables , saveAs = 'EW' , Channels = Channels)


Tables    = np.load('Numpys/PPPC_Tables_EW.npy', allow_pickle=True).item()
Extract_Limits_SingleDwarf(Dwarves_List = Dwarves_List , Masses = Masses , Tables =  Tables , saveAs = 'noEW')
Extract_Limits_Combined   (Dwarves_List = Dwarves_List , Masses = Masses , Tables =  Tables , saveAs = 'noEW' , Channels = Channels)











