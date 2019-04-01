#!/usr/bin/python

import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.optimize import brute
from scipy.optimize import fmin
from scipy.special import gammainc
from math import pi


'''
Federico's modification:
- the list of dwarves is now read directly from the dSph_jfac_file files containing the Jfactors (so that the order is always preserved?)
- dSph_ll_files is created form the list  of dwarves
- the Fermi_sigmav_lim now includes both the sigma_v and p_value calculation (to be set with the flag == True )
- the Fermi_sigmav_lim receives x and dndlox as an input (to be read externally form the dictionaries of the Tables)
'''

'''
JH modification:
- In marg_like_dw():
    res = minimize_scalar(chi2min) -> res = minimize_scalar(chi2min,method='bounded',bounds=(-5.0,5.0))
- In Fermi_sigmav_lim():
    - changed minimization routine for sigmav, now very stable and only 15% slower than brent
    - sigmavmin and sigmavmax are now arguments of Fermi_sigmav_lim(), they define the allowed range (can be choosen very large)
    - always compute the pvalue in the end (only one run -> fast!)
    - assign sigmavmin and sigmavmax for pvalue = 1 and 0, respectively (limit outside rage)
    - allow for setting cl_val (=0.95 by default)
'''

# number of bins in data
nBin = 24
j0 = 3.086e21 # convention spectra

dSph_jfac_file = 'Jfactors.dat'
dSph_ll_files_path = 'likelihoods/'
# list has to match the order of dwarfs in dSph_jfac_file!





# This function reads the list of dwarves from the Jfactor.dat file
def extract_dwarveslist(dSph_jfac_file):
    dwarflist_all = []
    op = open(dSph_jfac_file,'r')
    for line in [ line for line in op.readlines() if 'Row' in line]:
        dwarflist_all.append (line.split(' ')[3].replace('\n',''))
    return dwarflist_all
                              

# print dwarflist_all = extract_dwarveslist(dSph_jfac_file)

def eflux(spectrum, emin=1e2, emax=1e5, quiet=False):
    """ Integrate a generic spectrum, multiplied by E, to get the energy flux.
    """
    espectrum = lambda e: spectrum(e)*e
    tol = min(espectrum(emin),espectrum(emax))*1e-10
    try:
        return quad(espectrum,emin,emax,epsabs=tol,full_output=True)[0]
    except Exception, msg:
        print('Numerical error "%s" when calculating integral flux.' % msg)
    return np.nan


# F:
# dictionary to include Fermi-LAT likelihoods from dwarfs listed in dwarf_list
# dwarf_list should includes only the one I want to include in the calculation of the limits
# the complete list of dwarves is read from the Jfactor.dat file by the function extract_dwarveslist

def dw_dic(dwarf_list = ''):
    
    global dSph_jfac_file, dSph_ll_files_path, nBin

    dwarflist_all = extract_dwarveslist(dSph_jfac_file) # create the list of dwarves reading the Jfactor dat file
    dSph_ll_files = [ 'like_' + dwarf + '.txt' for dwarf in dwarflist_all ]
    
    jbar_dSph = np.loadtxt(dSph_jfac_file, unpack=True)[3]
    jbar_dSph_error = np.loadtxt(dSph_jfac_file, unpack=True)[4]
    
    dw_dic_coll = {}
    
    for dwarf in dwarflist_all:

      for D in dwarf_list:
        if D == dwarf:
        
          elem = 'like_'+str(dwarf)+'.txt'
        
          if elem in dSph_ll_files:
            dwindex = dSph_ll_files.index(elem)
            likefile = dSph_ll_files[dwindex]
            data = np.loadtxt(dSph_ll_files_path+likefile, unpack=True)
            efluxes = (1e-3*data[2]).reshape(nBin,-1) # convert flux list to 2D list of fluxes for all ebins, convert to GeV
            logLikes = data[3].reshape(nBin,-1)
            
            #            likes = [ interp1d(f,l-l.max(),bounds_error=False, fill_value=-1e5) for f,l in zip(efluxes,logLikes) ] # likes[i](flux) gives likelyhood of i'th ebin at flux[GeV]
            likes = [ interp1d(f,l,bounds_error=False, fill_value=-1e5) for f,l in zip(efluxes,logLikes) ] # likes[i](flux) gives likelyhood of i'th ebin at flux[GeV], fill_value for fluxes outside the given range (just very bad ll)
            
            ll_null = 0.0
            for like in likes:
                ll_null+=like(0)
        
            jfact = jbar_dSph[dwindex]
            jfacterr = jbar_dSph_error[dwindex]
            
            dict = {
                    'Jfac': jfact,
                    'Jfac_err': jfacterr,
                    'll_null': ll_null,
                    'likelihood': likes,
            }
    
            dw_dic_coll[dwarf] = dict
          else:
            print('WARNING: "%s" not found and, hence, not taken into account!' % dwarf )

#print "dwarfs included:", dw_dic_coll.keys()
    #s    print dw_dic_coll
    #raw_input(' ')
    return dw_dic_coll




def compute_pvalue(ll_tot,ll_null):
    
    pvalue1 = lambda x: 1-gammainc(1/2.0,x/2.0)
    ts = -2*ll_tot+2*ll_null
    oneortwosidedfactor = 2
    
    if ts>=0.0:
        pval = pvalue1(ts)/oneortwosidedfactor
    else:
        if oneortwosidedfactor < 2:
            pval=1
        else:
            pval = 1-pvalue1(-ts)/oneortwosidedfactor

    return 1-pval


# marginalize over J-factor of a certain dwarf:
def marg_like_dw(dw_in_i,pred,marginalize):
    
    global j0, nBin
    j,jerr,like_inter = dw_in_i['Jfac'], dw_in_i['Jfac_err'], dw_in_i['likelihood']
    
    # function to be minimized:
    def chi2min(x):
        
        flux_like = 0.0
        
        for i in range(nBin):
            
            like_i = like_inter[i]
            pred_i = pred[i]
            flux = pred_i*10**(j+x*jerr)/j0
            flux_like += like_i(flux)
        
        jfac_like = - 0.5*x**2
        
        # return chi^2:
        return -2.0*(flux_like+jfac_like)
    
    if marginalize:
        res = minimize_scalar(chi2min,method='bounded',bounds=(-5.0,5.0))
        jsigma = res.x
        ll_max = -0.5*res.fun
    else:
        ll_max = -0.5*chi2min(0.0)
        jsigma = 0.0
    
    # return minimal ll
    return ll_max, jsigma

# total log-likelihood and pvalue (with or without marginalization):
def res_tot_dw(dw_in,pred,marginalize):
    
    ll_tot = 0.0
    ll_null = 0.0
    j_factors = {}
    
    for k,v in dw_in.iteritems():
        marg_like = marg_like_dw(v,pred,marginalize)
        ll_tot += marg_like[0]
        ll_null += v['ll_null']
        j_factors[k] = marg_like[1]
    
    pval = compute_pvalue(ll_tot,ll_null)
    return ll_tot, ll_null, pval, j_factors



# function to compute UL on sigmav (needs dw_in=dw_dic() to be loaded in advance)
# F: modified so that the input are directly x and dndlogx (to be extracted from the dictionaries before calling the function)
# This function now includes the calculation of the sigmav_ul and the p_value (if set the flag == True in the parameters of the function)
def Fermi_sigmav_lim_Twosided(mDM, x = '' , dndlogx = '' , dw_in = '' , marginalize = True, sigmavmin=1e-35, sigmavmax=1e-15, step_size_scaling=1.0, cl_val = 0.95):

    np.seterr(divide='ignore', invalid='ignore')   # Keep numpy from complaining about dN/dE = 0...
    
    global j0, nBin
    
    # DM predicitons
    # upload the spectral file
    # Spectral file created assuming J=10^18 GeV^2/cm^5, sigmav=1e-25 cm^3/s (this is a nomralization by fermi...)
    j0 = 3.086e21 # convention spectra
    sigmav0 = 1e-26

    emins = [0.5, 0.666760716, 0.8891397050000001, 1.1856868500000002, 1.5811388300000002, 2.10848252, 2.81170663, 3.7494710500000004, 5.0, 6.667607159999999, 8.89139705, 11.856868500000001, 15.8113883, 21.0848252, 28.117066299999998, 37.494710500000004, 50.0, 66.6760716, 88.91397049999999, 118.568685, 158.11388300000002, 210.848252, 281.170663, 374.94710499999997]
    emaxs = [0.666760716, 0.8891397050000001, 1.1856868500000002, 1.5811388300000002, 2.10848252, 2.81170663, 3.7494710500000004, 5.0, 6.667607159999999, 8.89139705, 11.856868500000001, 15.8113883, 21.0848252, 28.117066299999998, 37.494710500000004, 50.0, 66.6760716, 88.91397049999999, 118.568685, 158.11388300000002, 210.848252, 281.170663, 374.94710499999997, 500.0]

    # Load the spectrum E, dN/dE
    #energy,dnde = np.loadtxt(specfile,unpack=True)
    #Load the spectrum in logx, dN/dlogx -> contained in the dictionary of dictionaries
    logx = np.log10(x)


    mDM = eval(mDM) # must be in GeV

    energy = mDM*10**logx

    dnde = (dndlogx/(mDM*10**logx*2.30259))
    log_energy = np.log10(energy)
    log_dnde = np.log10(dnde)
    log_interp = interp1d(log_energy,log_dnde)
    #print ' ' , energy
    spectrum = lambda e: np.nan_to_num(10**( log_interp(np.log10(e)) )) if (e <= energy.max() and e >= energy.min()) else 0.0
    
    #### prediction from DM point for sigmav_0:
    pred = np.array([eflux(spectrum,e1,e2)/mDM**2*sigmav0*j0/(8.*pi) for e1,e2 in zip(emins,emaxs)])
    
    
    def find_sigmav(x,pred,dw_in,marginalize):
        
        pred_sigma = pred*10**(-x)/sigmav0
        pvalue = res_tot_dw(dw_in,pred_sigma,marginalize)[2]
        
    
        
#        print "   ",10**(-x), pvalue
        atanhpval = np.arctanh(pvalue - 1e-9)
        atanclval = np.arctanh(cl_val - 1e-9)
        return (atanhpval-atanclval)**2


    #DIC = { 'Brent':[] , 'Bounded': [] ,}
    find_sig = lambda x: find_sigmav(x,pred,dw_in,marginalize)

    # brute methode:
    brute_range_min = -np.log10(sigmavmax)
    brute_range_max = -np.log10(sigmavmin)
    if marginalize:
        num_steps = int(step_size_scaling*2.0*(brute_range_max-brute_range_min))
    else:
        num_steps = int(step_size_scaling*5.0*(brute_range_max-brute_range_min))

    res = brute(find_sig,[(brute_range_min,brute_range_max)], Ns=num_steps, full_output=False, finish=fmin)
    sigmav_ul = 10**(-res[0])
    
    p_value = -1
    
    pred_sigma = pred*sigmav_ul/sigmav0
    result  = res_tot_dw(dw_in,pred_sigma,marginalize)
    p_value = result[2]
    

    if p_value <= cl_val*0.98:
        sigmav_ul=sigmavmax
        print " WARNING: increase range (sigmavmin,sigmavmax) and/or step_size_scaling!"
    elif p_value >= cl_val*1.02:
        sigmav_ul=sigmavmin
        print " WARNING: increase range (sigmavmin,sigmavmax) and/or step_size_scaling!"

    return [sigmav_ul , p_value]






