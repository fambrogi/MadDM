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
xsections_dic = { 'z' : { '1': { 'abs':  [96.5 , 12.4 , 0.6 ]  , 'rel': [1 , 12.4/96.5  , 0.6/96.5   ] }   ,
	                  '3': { 'abs':  [18.63 , 5.51, 0.73]  , 'rel': [1 , 5.51/18.63 , 0.73/18.63 ] }   ,
	                  '10': { 'abs':  [3.06, 1.71,   0.41] , 'rel': [1 , 1.71/3.06  , 0.411/3.06 ] } } , 



		  'a' : { '1': { 'abs':  [96.5 , 10.76 , 1.087 ] , 'rel': [1 , 10.76/96.5  , 1.087/96.5 ] }   , # ok
	                  '3': { 'abs':  [18.63 , 3.94, 0.32]    , 'rel': [1 , 3.94/18.63 , 0.32/18.63  ] }   , # ok
	                 '10': { 'abs':  [3.06, 1.08,   0.148]    , 'rel': [1 , 1.08/3.06  , 0.12/3.06  ] } } , # ok

	          'h' : { '1': { 'abs':  [96.5 , 0.184 , 0.0007 ] , 'rel': [1 , 0.18/96.5  , 0.0007/96.5   ] }   ,
	                  '3': { 'abs':  [18.63 , 0.05, 0.0005]   , 'rel': [1 , 0.05/18.63 , 0.0005/18.63  ] }   ,
	                 '10': { 'abs':  [3.06, 0.012,   0.0079]  , 'rel': [1 , 0.012/3.06  , 0.0079/3.06  ] } } , 

		  'x' : { '1': { 'abs':  [96.5 , 23.1 , 0.6 ]  , 'rel': [1 , 23.1/96.5  , 0.6/96.5   ] }  ,
	                  '3': { 'abs':  [18.63 , 5.51, 0.73]  , 'rel': [1 , 5.51/18.63 , 0.73/18.63 ] }  ,
	                  '10': { 'abs': [3.06, 1.71,   0.41] , 'rel': [1 , 1.71/3.06  , 0.411/3.06  ] } } , # x TO DO!!!



 } # all ok




'''
xsections_1_zz = xsections_dic['z'][]
xsections_3_zz = xsections_dic['z'][]
xsections_10_zz = xsections_dic['z'][]

xsection_plot (x1=xsections_1_zz , x2=xsections_3_zz , x3=xsections_10_zz )
'''



