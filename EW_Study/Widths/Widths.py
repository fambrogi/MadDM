import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt 
import os,sys
import numpy as np
"""
Values of the widths of y0 for different configurations 
"""
# mxd  = 1000.0
# beam = 1001.0
# with of the higgs set to 1e-03

my_1 = np.array( [100  ,    200      , 500   , 1000 , 5000 , 10000 , 15000 , 20000 , 50000 , 100000  ] )
wi_1 = np.array( [4.18e-5 , 6.08e-03 , 0.255 , 2.27 ,  451 , 2760 ,  8636 , 19880 , 300000 , 2391000 ] )

my_1 = my_1 / 1000.
wi_1 = wi_1 / 1000.
##############################################################################################################

# mxd  = 1000.0
# beam = 1001.0
# with of the higgs set to auto
# they are exactly the same
my = [100  ,    200      , 500   , 1000 , 5000 , 10000 , 15000 , 20000 , 50000 , 100000  ]
wi = [4.48e-5 , 6.08e-03 , 0.255 , 2.27 ,  451 , 2760 ,  8636 , 19880 , 300000 , 2391000 ]

##############################################################################################################


font = 13
# Plotting 
plt.yscale('log')
plt.xscale('log')

plt.xlim(0.01 , 1000)
plt.grid(color = 'lightgray', linestyle = ':')
plt.xlabel(r'Mediator Y0 Mass [TeV]'  , fontsize = font)
plt.ylabel(r'Mediator Y0 Width [TeV]' , fontsize = font)
plt.xticks(my_1, my_1, rotation = 45, fontsize = font-4)
plt.plot   (my_1, wi_1 ,    color = 'blue'  , linestyle = '--' , label = r'$m_{\chi _D}$')
plt.plot   (my_1, my_1/10 , color = 'lightgray'  , linestyle = '-', label = r'$w_{y0}=10\%(m_{y0})$' )
plt.legend(fontsize = font - 1 , loc = 'lower right')
plt.scatter(my_1, wi_1,     color = 'orange', marker = 'o')
plt.savefig('Widths_check.pdf', bbox_inches = 'tight')
plt.close()

# mxd  = 1000.0
# beam = 1001.0
# with of the higgs set to auto
# they are exactly the same
#my = [100  ,    200      , 500   , 1000 , 5000 , 10000 , 15000 , 20000 , 50000 , 100000  ]
#wi = [4.48e-5 , 6.08e-03 , 0.255 , 2.27 ,  451 , 2760 ,  8636 , 19880 , 300000 , 2391000 ]



