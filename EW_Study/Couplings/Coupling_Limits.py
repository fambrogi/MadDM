"""Coupling limits not to violate unitarity 
   as in arXiv:1510.02110v2  

   s < (pi * my0 **2)/ (gy**2 * mx) => gy**2 < (pi * my0**2)//(sqrts * mx)

   Args:
        mx: dark matter mass
        my0: mediator mass
        gy: coupling x,y0
        sqrts: centre-of-mass energy
"""

import os,sys
import math 
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm



pi = math.pi


def max_g(my0= 1. , sqrts= 1., mx = 1.):
    """ calculates the maximum allowed value for the coupling constant given sqrts and my0,
        for a specific mx mass """
    
    v = math.sqrt( (pi * my0**2)/(sqrts * mx) )
    return v


def min_y0(sqrts = '', g = '', mx = ''):
    """ calulates the minimum value of y0 for unitarity """
    
    y = math.sqrt( sqrts * g**2 * mx / pi )
    return y



'''
mx = 1000.
my0 = 100.

prova = max_g(my0=my0 , sqrts=sqrts, mx=mx)    
    
    
MY = [1 + i*200 for i in range(50)]
S = [2*mx +i*10 for i in range(50)]
'''

def create_grid(mx=''):
    MY, S = [], []
    if mx == '1000': 
        mx = eval(mx)
        MY = [1 + i*200 for i in range(50)]
        S = [2*mx +i*10 for i in range(50)]        
        
    elif mx == '10000':
        mx = eval(mx)        
        MY = [1 + i*500 for i in range(50)]
        S = [2*mx +i*50 for i in range(50)]
        
    elif mx == '100000':
        mx = eval(mx)        
        MY = [1 + i*5000 for i in range(50)]
        S = [2*mx +i*500 for i in range(50)]
        
        
    Y, X, Z = [],[],[]    
    for y in MY:
        for s in S:
            v = max_g(my0=y , sqrts=s, mx=mx)
            X.append(s)
            Y.append(y)
            Z.append(v)            
            
    return X,Y,Z 




fnt = 16


def text(mx=''):
    if mx == '1000':
        plt.text(2020, 9100, r'$m_{\chi}=$ 1 [TeV]' , fontsize = fnt-1)
    if mx == '100000':
        plt.text(202000, 230000, r'$m_{\chi}=$ 100 [TeV]' , fontsize = fnt-1)
    if mx == '10000':
        plt.text(20200, 23000, r'$m_{\chi}=$ 10 [TeV]' , fontsize = fnt-1)

    plt.xlabel( r'$\sqrt{s}$ [GeV]', fontsize = fnt)
    plt.ylabel( r'$m_{y0}$ [GeV]', fontsize = fnt)


def plot_coupling_my0_sqrts(mx = '1000', x= '', y='', z=''):
    
    text(mx=mx)
    plt.hist2d(x, y, bins=[50,50] , norm = LogNorm(), weights=z)
    cb = plt.colorbar()
    cb.ax.set_ylabel(r'Max($g_{Sw}$)', fontsize = fnt)
    cb.ax.tick_params(labelsize=fnt-4)
    
    plt.savefig('PLOTS/coupling_constant_ul_Mxd_' + mx + '_Log.pdf' , bbox_inches = 'tight')
    plt.close()



    text(mx=mx)
    plt.hist2d(x, y, bins=[50,50], weights=z)
    cb = plt.colorbar()
    cb.ax.set_ylabel(r'Max($g_{Sw}$)', fontsize = fnt)
    cb.ax.tick_params(labelsize=fnt-4)
    
    plt.savefig('PLOTS/coupling_constant_ul_Mxd_' + mx + '.pdf' , bbox_inches = 'tight')
    plt.close()    
    
    '''
    text(mx=mx)
    plt.hist2d(x, y, bins=[50,50], weights=z)
    cb = plt.colorbar()
    cb.ax.set_ylabel(r'Max($g_{Sw}$)', fontsize = fnt)
    cb.ax.tick_params(labelsize=fnt-4)
    if mx == '1000':
        plt.xlim(2000, 2010)
        plt.ylim(0, 2010)

    plt.savefig('PLOTS/coupling_constant_ul_Mxd_' + mx + '_zoom.pdf' , bbox_inches = 'tight')
    plt.close()
    '''
    
    
    
    
'''
M = ['1000','10000','100000']

for m in M:
    X,Y,Z = create_grid(mx=m)
    print('for m= ', m , ' the data is: ', X,Y,Z)
    plot_coupling_my0_sqrts(mx = m, x=X, y=Y, z=Z)
'''



Ms = [0.5 , 1 , 5 , 10 , 50, 100]
Qs = [ 2.*n+2.*n/1000. for n in Ms ]

Gs = [6.28, 1 , 0.5, 0,1 , 0.05, 0,01 , 0.005]

print Ms, Qs

res = {}

for g in Gs:
    res[g] = []
    for m,s in zip(Ms,Qs):

        y =  min_y0(sqrts = s, g = g, mx = m)
        res[g].append(y)
        print 'mX , mY, sqrts, g ' , m , y , s , g   



print res
