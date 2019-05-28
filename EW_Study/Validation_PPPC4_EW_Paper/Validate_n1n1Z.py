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

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)



def Apply_Plot_Properties(x_label = True, y_label = True):
      ### Plotting Part, same for each plot
      SIZE = 25
      THICK_LABEL_SIZE = 20
      if y_label: plt.ylabel(r'$\frac{dN}{dlogx}$'     , fontsize = SIZE)
      if x_label: plt.xlabel(r'$x= \frac{K}{m_{ \chi}}$'  , fontsize = SIZE)
      plt.xlim(0.000007, 1)
      plt.ylim(0.01, 400)
      plt.yscale('log')
      plt.xscale('log')
      plt.tick_params(axis='both', which='major', labelsize=THICK_LABEL_SIZE, length=10, width=1.1, top='off', right='off')
      plt.tick_params(axis='both', which='minor', labelsize=THICK_LABEL_SIZE, length=7 , width=1.1, top='off', right='off')

# Summary of the dictionary in the PPC Tables:
# keys of the dic: ['antiprotons', 'gammas', 'Masses', 'neutrinos_mu','positrons', 'Particle_Spectra', 'x', 'DM_Channels', 'neutrinos_e', 'neutrinos_tau']
# a['gammas']['5.0']['ee']
# channels: ['mumu', 'qq', 'tautau', 'bb', 'gammagamma', 'tt', 'gg', 'WW','cc', 'hh', 'ZZ', 'ee']
# a['x'] = values of the x variable , x = E_kin/m_DM



######
import math
DM = 3000
def dnz_dx(x, dm = ''):
    alpha2 = 1
    pi = math.pi
    cw = 1
    mw = 80.3
    e = mw/dm
    factor = alpha2/pi * cw**2
    first =   (9*x**4 - 18*x**3 + 25*x**2 -16*x +8 )/(2*x*(1-x)) * math.log( (2*x/e) / (math.sqrt(1-x+x**2) ) ) 
    second =  2*( -3*x**5 + 16*x**4 -37*x**3 +42*x**2 -24*x +8)/( (2-x)**3 * (1-x) *x  ) * math.log(1-x)
    third = -(52 - 176*x + 271*x**2 -247*x**3 + 150*x**4 -55*x**5 +9*x**6)*x/(2*(2-x)**2 * (1-x)*(1-x+x**2) )
    res = 0.005 * (first+second+third)
    return res

def dna_dx(x, dm=""):
    alpha_em = 1/137.
    e = 80.3/dm
    factor = alpha_em / np.pi
    first = 4*(1-x+x**2)**2/(x*(1-x))*np.log(2/e)  
    second = 2*( 4 -12*x + 19*x**2 -22*x**3 +20*x**4 -10*x**5 +2*x**6)/((x-2)**2 * (x-1)*x)
    third = np.log(1-x)*(-6*x**5 + 32*x**4-74*x**3+84*x**2-48*x+16)/( (x-2)**3 * (x-1) * x )
    factor = factor / 1.7
    res = factor*(first + second + third)
    #print x, first, second, third
    return res

# *************************************************************************************************************************************************
# Files
Z_Ma5_old = "Zboson_energy.txt"
Z_Ma5_schannel = "n1n1_wwz_onlyzschannel.txt"


ma = open(Z_Ma5_old, 'r').readlines()
ma5_values = [ x.replace("\n","") for x in ma if '3100' not in x and 'progress' not in x and x ]
ma5_values_cleaned = [ eval(x) for x in ma5_values if x]
ma5_values_old = [ eval(x)/DM for x in ma5_values if x and x !=0]

ma_s = open(Z_Ma5_schannel, 'r').readlines()
ma5_values = [ x.replace("\n","") for x in ma_s if '3100' not in x and 'progress' not in x and x ]
ma5_values_cleaned_s = [ eval(x) for x in ma5_values if x]
ma5_values_schannel = [ eval(x)/DM for x in ma5_values if x and x !=0] # calculating x = E/DM


#ma5_100TeV = open('ma5_n1n1_wwz_100TeV.txt','r').readlines()
#ma5_values_100 = [ x.replace("\n","") for x in ma5_100TeV if '3100' not in x and 'progress' not in x and x ]
#ma5_values_cleaned_s_100 = [ eval(x) for x in ma5_values_100 if x]
#ma5_values_schannel_100 = [ eval(x)/100000.0 for x in ma5_values_100 if x and x !=0] # calculating x = E/D

nunu_3TeV = open('Res_new/nunu_wwz_3TeV.txt','r').readlines()
nunu_3TeV =  [ eval(x.replace("\n","")) for x in nunu_3TeV if 'progress' not in x and x !="\n"]
nunu_3TeV_n = [ x/3000. for x in nunu_3TeV if x and x !=0 and x < 2900] # calculating x = E/DM


n1n1_ch80_3TeV = open('Res_new/n1n1_wwz_only_ch80_3TeV.txt','r').readlines()
n1n1_ch80_3TeV =  [ eval(x.replace("\n","")) for x in n1n1_ch80_3TeV if 'progress' not in x and x !="\n"]
n1n1_ch80_3TeV_n = [ x/3000. for x in n1n1_ch80_3TeV if x and x !=0 and x < 2900] # calculating x = E/DM  


# histo properties
range_h = [0.01, 1]
bins = 25
scale = 0.17
X = [] ### contains the x values and the y values (ready for plotting)
values,edges = np.histogram(ma5_values_schannel , bins = bins, range = range_h, density = True )
for v,e in zip(values,edges):
    X.append(v*e*scale)
plt.plot(edges[:len(X)], X, color = 'lime', label = r'MadDM (only z s-chan.), $m_{\tilde \chi_1 ^0}$= 3 TeV' , ls = '-')


X = [] ### contains the x values and the y values (ready for plotting)                                                                                                                                                                                                                   
values,edges = np.histogram(n1n1_ch80_3TeV_n , bins = bins, range = range_h, density = True )
for v,e in zip(values,edges):
    X.append(v*e*scale)
plt.plot(edges[:len(X)], X, color = 'lime', label = r'MadDM ($m_{\tilde \chi _1 ^{\pm}}$=80 GeV), $m_{\tilde \chi_1 ^0}$= 3 TeV' , ls = '--')


Z_yellow = "Z_paper_yellow.txt"
x,y, = np.loadtxt(Z_yellow, unpack = True)

# calculating from analytical equation
x_eq = [0.001 + i*0.0005 for i in range (1998) ]
y_eq = [ dnz_dx(i, dm=DM) for i in x_eq ] 
#y_eq_100TeV  = [ dnz_dx(i, dm=100000) for i in x_eq ] 

# digitized plot
plt.plot(x,y, color = 'yellow', label = r'Paper (Digitized plot), $m_{\tilde \chi_1 ^0}$= 3 TeV' , ls = '--')
# analytical plot
plt.plot(x_eq, y_eq ,        label = r"Eq.B.64 $m_{\tilde \chi_1 ^0}$= 3 TeV" , color = 'orange' , ls = '--')




#plt.plot(x_eq, y_eq_100TeV , label =r"Eq. B.64 ($m_{\tilde \chi_1 ^0}$= 100 TeV)" , color = 'orange' )
#lab_wwz = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ z, \ m_{\tilde \chi_1 ^0}=$ 3 TeV'
#plt.plot(edges[:len(X)], X, label = lab_wwz, color = 'red' )
# old (with t-channels charginos, higgses)
#plt.hist(n1n1_ch_3TeV_n,      bins, histtype="step", color = 'blue', label = 'MadDM (with ch1 t-chan.) 3 TeV' , normed = True)
# old ( only s-channel Zs)

# 100 TeV
#plt.hist(ma5_values_schannel_100, bins, histtype="step", color = 'cyan', label = 'MadDM (only z s-chan.) 100 TeV' , normed = True)

# *************************************************************************************************************************************************
# properties
plt.yscale('log')
plt.xscale('log')
plt.title(r'$n_1 n_1 \rightarrow W^- W^+ Z$', y=1.03)
plt.xlim(0.009,1.1)
plt.ylim(0.01,10)
majorLocator = MultipleLocator(20)
majorFormatter = FormatStrFormatter('%d')
minorLocator = MultipleLocator(5)
axes = plt.subplot(111)
axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for tick in axes.xaxis.get_minor_ticks():
                tick.label.set_fontsize(5) 
                # specify integer or one of preset strings, e.g.
                #tick.label.set_fontsize('x-small') 
                tick.label.set_rotation('vertical')
for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(8) 
                tick.label.set_rotation('vertical')
plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.grid(which='major', linestyle='--', color = 'lightgray', lw = 1.05)
plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)
plt.legend(loc = 'upper right' , fontsize = 7)
plt.xlabel(r"$x = \frac{E}{m_{DM}} $")
plt.ylabel("Normalized Counts /"+str(bins)+'GeV')
plt.savefig('plots/z_comparison_new.pdf', bbox_inches = 'tight')
plt.close()


# *************************************************************************************************************************************************
# ma5_values_cleaned_s
plt.title(r'$n_1 n_1 \rightarrow W^- W^+ Z$', y=1.03)
bins = 50
axes = plt.subplot(111)
plt.yscale('log')
plt.xscale('log')

majorLocator = MultipleLocator(20)
majorFormatter = FormatStrFormatter('%d')
minorLocator = MultipleLocator(5)
axes = plt.subplot(111)
axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for tick in axes.xaxis.get_minor_ticks():
                tick.label.set_fontsize(5)
                # specify integer or one of preset strings, e.g.                                                                                                                                                                                                             
                #tick.label.set_fontsize('x-small')                                                                                                                                                                                                                          
                tick.label.set_rotation('vertical')
for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(8)
                tick.label.set_rotation('vertical')


                
lab_ch80 = r'MadDM ($m_{\tilde \chi _1 ^{\pm}}$=80 GeV), $m_{\tilde \chi_1 ^0}$= 3 TeV'
range_h = [0.01, 1]
bins = 30
scale = 0.17
X = [] ### contains the x values and the y values (ready for plotting)                                                                                                                                                                                                      
values,edges = np.histogram( n1n1_ch80_3TeV_n, bins = bins, range = range_h, density = True )
for v,e in zip(values,edges):
    X.append(v*scale)
#plt.plot(edges[:len(X)], X, color = 'orange', label = lab_ch80 , ls = '-')

y = np.ndarray.tolist (4 * np.array(y) )
print y
plt.plot(x,y, color = 'yellow', label = r'Paper Dig. plot (*factor 4), $m_{DM}$= 3 TeV' , ls = '--')

y_eq = np.ndarray.tolist (4 * np.array(y_eq) )
plt.plot(x_eq, y_eq ,        label = r"Eq.B.64 (*factor 4) $m_{DM}$= 3 TeV" , color = 'orange' , ls = '--')



plt.hist(n1n1_ch80_3TeV_n,  bins, histtype="step", color = 'blue',   label = r'MadDM ($m_{\tilde \chi _1 ^{\pm}}$=80 GeV), $m_{\tilde \chi_1 ^0}$= 0.5 GeV, CM=3 TeV' , density = True)

lab_nu = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+ z, \ CM=$ 3 TeV'

plt.hist(nunu_3TeV_n,  bins, histtype="step", color = 'cyan',   label = lab_nu, density = True )
plt.hist(ma5_values_schannel,  bins, histtype="step", color = 'lime', label = 'MadDM (only z s-chan.)' , density = True)
plt.ylim(0 , 10)
plt.xlim(0.009, 1)
plt.ylabel("Normalized Counts /"+str(bins)+'GeV')
plt.xlabel("Z energy [GeV]")
plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.legend(loc = 'upper left', fontsize = 7)
plt.savefig('plots/kinematic_histo.pdf', bbox_inches = 'tight')
plt.close()
# *************************************************************************************************************************************************



############################ GAMMA ANALYSIS

samples = ['Res_new/n1n1_wwa_1TeV.txt',           'Res_new/n1n1_wwa_10TeV.txt' ,
	   'Res_new/n1n1_wwa_only_100k_1TeV.txt', 'Res_new/n1n1_wwa_only_100k_10TeV.txt',
	   'Res_new/n1n1_wwa_only_ch80_1TeV.txt','Res_new/nunu_wwa_10TeV.txt',
           #'Res_new/nunu_ww_wwa_1TeV.txt' 
]






masses = [1000, 10000, 1000, 10000, 1000, 10000, 1000]
v = 6.5
scales = [v,v,v,v,v,v,y]
# histo properties
range_h = [0.01, 1]
bins = 25

X, edges = [],[] ### contains the x values and the y values (ready for plotting)
for s,dm,scale in zip(samples, masses, scales):
    val = []
    fi = open(s, 'r').readlines()
    values   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n = [ x/dm  for x in values if x] 
    h,e = np.histogram(values_n , bins = bins, range = range_h, density = True )
    edges.append(e)

    for h,b in zip(h,e):
        val.append(h*b/scale)
    X.append(val)


# PLOT as paper

plt.title(r'$n_1 n_1 \rightarrow W^- W^+ \gamma$', y=1.03)

axes = plt.subplot(111)
plt.xlim(0.002 , 1.1 )
plt.ylim(0.01, 0.1)
plt.yscale('log')
plt.xscale('log')
plt.ylim(0.01, 1)
plt.ylabel(r'$xdN_{\gamma}/dx$')
plt.xlabel('x = E/DM')
plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.grid(which='major', linestyle='--', color = 'lightgray', lw = 1.05)
plt.grid(which='minor', linestyle=':' , color = 'lightgray', lw = 1.05)


axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for tick in axes.xaxis.get_minor_ticks():
                tick.label.set_fontsize(5) 
                # specify integer or one of preset strings, e.g.
                #tick.label.set_fontsize('x-small') 
                tick.label.set_rotation('vertical')
for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(8) 
                tick.label.set_rotation('vertical')

# official line from paper
x_10, y_10 = np.loadtxt('10TeV_gamma.csv', unpack = True)
x_1 , y_1  = np.loadtxt('1TeV_gamma.csv' , unpack = True)
plt.plot(x_10, y_10, color = 'blue', label = r'Digitized $m_{DM}$=10 TeV' , ls = ':')
plt.plot(x_1, y_1  , color = 'red' , label = r'Digitized $m_{DM}$=1 TeV' , ls = ':')
# calculating from analytical equation
DM = 1000
x_eq = [0.001 + i*0.0005 for i in range (1998) ]
x_eq = [ x for x in x_eq if x < 1 and x> 0]
y_eq_1TeV  = [ i*dna_dx(i, dm=DM) for i in x_eq ]
plt.plot(x_eq , y_eq_1TeV , color = "black", label = 'Equation B62.a, $m_{DM}$=1 TeV')
 



# labels
l_1_noch  = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma, \ m_{\tilde \chi_1 ^0}=$ 1 TeV' 
l_10_noch = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma, \ m_{\tilde \chi_1 ^0}=$ 10 TeV'
l_1_c     = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan.(80GeV),  1 TeV'
l_10_c    = r'MadDM $\tilde \chi_1 ^0 \tilde \chi_1 ^0  \rightarrow w^- w^+ \gamma$ with $\tilde \chi_1 ^{\pm}$ t-chan. 10 Tev'
l_nu_1    = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+ \gamma, \ CM=$ 1 TeV'  
l_nu_10   = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+ \gamma, \ CM=$ 10 TeV'  
l_nu_1_a   = r'MadDM $\nu_e \bar \nu_e \rightarrow w^- w^+, w^- w^+ \gamma, \ CM=$ 1 TeV' 
 
labels = [l_1_noch , l_10_noch, l_1_c, l_10_c , l_nu_1, l_nu_10, l_nu_1_a ]
colors = ['red','blue','red','blue','orange','cyan', 'lime']
styles = ['--','--','-','-','--','--',':']

for e,y,c,l,s in zip (edges,X,colors,labels,styles):
     plt.plot(e[:len(y)], y, color = c, label = l , ls = s)


plt.legend(loc = 'upper left', fontsize = 8)
plt.savefig('plots/Gammas_Validation.pdf', bbox_inches = 'tight')
plt.close()



'''
# *************************************************************************************************************************************************
# old kinematic

plt.title(r'$n_1 n_1 \rightarrow W^- W^+ \gamma$', y=1.03)

bins = 100
axes = plt.subplot(111)
axes.xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))


a = plt.hist(ma5_values_1_f, bins, range=[0,10000], histtype="step", color = 'blue',  label = label_1, density = True)
plt.hist(ma5_values_10_f   , bins, range=[0,10000], histtype="step", color = 'lime',  label = label_10 , density = True)
plt.hist(ma5_values_10_c_f , bins, range=[0,10000], histtype="step", ls = '--', color = 'lime',  label = label_10_c , density = True)
plt.hist(ma5_values_10_cs_f , bins, range=[0,10000], histtype="step", ls = '--', color = 'green',  label = label_10_cs , density = True)
plt.hist(ma5_nu_f          , bins, range=[0,10000], histtype="step", color = 'slateblue',  label = label_nu , density = True)



plt.xlim(0, 10500)
plt.ylim(0.000001, 0.1)
plt.yscale('log')
plt.ylabel("Normalized Counts /"+str(bins)+'GeV')
plt.xlabel(r"$\gamma$ energy [GeV]")
plt.grid(linestyle= ':', color = 'lightgray', lw = 1.2 )
plt.legend(loc = 'upper left', fontsize = 10)
plt.savefig('simple_histo_gamma.pdf', bbox_inches = 'tight')
plt.close()

histo_1 , edges_1        = np.histogram(ma5_values_1_n , bins = bins, range = range_h, density = True)
histo_10, edges_10       = np.histogram(ma5_values_10_n, bins = bins, range = range_h,  density = True)
histo_10_cs, edges_10_cs = np.histogram(ma5_values_10_cs_n, bins = bins, range = range_h,  density = True)
histo_nu, edges_nu       = np.histogram(ma5_nu_n,        bins = bins, range = range_h,  density = True)

new_10,new_10_cs, new_1, nu_10 = [], [], [], []

len_1  = len(histo_1)
len_10 = len(histo_10)
len_nu = len(histo_nu)
len_10_cs = len(histo_10_cs)
for h,b in zip(histo_10_cs, edges_10_cs):
	new_10_cs.append(h*b/7)
for h,b in zip(histo_10, edges_10):
	new_10.append(h*b)
for h,b in zip(histo_1, edges_1):
	new_1.append(h*b)
for h,b in zip(histo_nu, edges_nu):
	nu_10.append(h*b/7)
'''





