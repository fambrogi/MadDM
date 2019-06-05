def selection_0():

    # Library import
    import numpy
    import matplotlib
    import matplotlib.pyplot   as plt
    import matplotlib.gridspec as gridspec

    # Library version
    matplotlib_version = matplotlib.__version__
    numpy_version      = numpy.__version__

    # Histo binning
    xBinning = numpy.linspace(8800.0,10002.0,22,endpoint=True)

    SCALE = 4/0.65

    dm = 10000
    fi = open('Res_new/mumu/xdxd_mumu.txt', 'r').readlines()
    values_mumu   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n_mumu = [2*x/dm  for x in values_mumu if x] 
 
    fi = open('Res_new/mumu/xdxd_mumu_all.txt', 'r').readlines()
    values_mumu_all   = [ eval(x.replace("\n","")) for x in fi if 'progress' not in x and x !="\n"]
    values_n_mumu_all = [ 2*x/dm  for x in values_mumu_all if x] 

    bins = 20
    lim = [0.88,1.0002]
    a = plt.hist(values_n_mumu, bins = bins, range = lim, color = 'blue', ls = '-', label = 'MadDM without EW' , histtype = 'step', density = True)
    c = plt.hist(values_n_mumu_all , bins = bins,range = lim, color = 'blue', ls = '--', label = 'MadDM with EW' , histtype = 'step', density = True)

    print a,c
    plt.rc('text',usetex=False)
    plt.xlabel(r"$2E_{T}(\mu^+)$/10 TeV", fontsize=16,color="black")
    plt.ylabel(r"$dN/dE_T$ $(\mu^+)$", fontsize=16,color="black")

    testo= r'EW: $x_d x_d \rightarrow \mu ^- \mu^+$'
    testo = testo + '\n+(' + r'$x_d x_d \rightarrow \mu ^- \mu^+ z$'
    testo = testo + '\n' + r'+$x_d x_d \rightarrow \mu ^- \mu^+ \gamma$'
    testo = testo + '\n' + r'+$x_d x_d \rightarrow \mu ^- \bar \nu_{\mu} w^+$'
    testo = testo + '\n' + r'+$x_d x_d \rightarrow \mu ^+ \nu_{\mu} w^- $)'

    plt.text(0.95 , 0.15 , testo ) # definition of EW

    plt.xlim(0.88, 1)
    plt.ylim(0.1,1000)
    plt.gca().set_xscale("linear")
    plt.grid(ls = ':', color = 'lightgray')
    plt.gca().set_yscale("log")

    import numpy as np
    x,y = np.loadtxt('lines_paper/mumu_histogram.csv', unpack = True)
    y = SCALE * np.array(y)
    plt.plot(x,y, color = 'black', ls = '-', label = 'arXiv:1001.3950 noEW')

    #x,y = np.loadtxt('lines_paper/mumu_histogram.csv', unpack = True)
    #x1 = 1000 * np.array(x)
    #plt.plot(x1,y, color = 'black', ls = '--', label = 'arXiv:1001.3950 EW')

    plt.legend(loc = 'upper left')
    plt.savefig('plots_new/mumu_validation.png', bbox_inches = 'tight')
    plt.close()
   



    bins = 50
    plt.ylim(1000,100000)
    plt.xlim(1000,5005)
    lim = [0,5005]
    a = plt.hist(values_mumu, bins = bins, range = lim, color = 'blue', ls = '-', label = 'MadDM without EW' , histtype = 'step')
    c = plt.hist(values_mumu_all , bins = bins,range = lim, color = 'blue', ls = '--', label = 'MadDM with EW' , histtype = 'step')
    plt.gca().set_yscale("log")
    plt.rc('text',usetex=False)
    plt.grid(ls = ':', color = 'lightgray')
    plt.xlabel(r"$E_{T}$ $\mu^+ $ [GeV] ", fontsize=16,color="black")
    plt.ylabel(r"$dN/dE_T$ $(\mu^+) $", fontsize=16,color="black")    
    plt.legend(loc = 'upper left')
    plt.savefig('plots_new/mumu_validation_basic.png', bbox_inches = 'tight')


# Running!
if __name__ == '__main__':
    selection_0()
