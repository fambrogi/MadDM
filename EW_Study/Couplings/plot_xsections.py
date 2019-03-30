import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import os,sys
import os.path


x_1TeV = [1000.1, 1001.0, 1010.0, 1100.0 ]
y_1TeV = [48.5  , 147.3,  90.86 , 4 ]
w_1TeV = r'$w_{y0}=1.9\times 10^1$ GeV'

x_10TeV = [10000.1, 10001.0, 10010.0, 10100.0, 11000.0]
y_10TeV = [0.0015 , 0.0048,   0.0152, 0.049,   0.19]
w_10TeV = r'$w_{y0}=1.9\times 10^1$ TeV'

x_100TeV = [100000.1,     100001.0,       100010.0,       100100.0,     101000.0 ,     110000.0]
y_100TeV = [4.8*10**(-8) , 1.57*10**(-7), 4.8*10**(-7) ,  1.52*10**(-6), 4.9*10**(-6),   2*10**(-5)]
w_100TeV = r'$w_{y0}=1.9\times 10^4$ TeV'



ebeam = r'$E_{beam} [GeV]$'
y = r'$\sigma _{\chi \chi \rightarrow W^- W^+}$ [pb]'

dic_prop = { '1'  :{'x': x_1TeV,  'y': y_1TeV,   'xlab': ebeam , 'ylab': y,'leg': w_1TeV   ,'ax':[-1,4,0.1,300], 
                    'c': 'blue'   } ,
             '10' :{'x': x_10TeV, 'y': y_10TeV,  'xlab': ebeam , 'ylab': y,'leg': w_10TeV  ,'ax':[-1,5,0.00001,1], 
                    'c': 'lime'   } ,
             '100':{'x': x_100TeV,'y': y_100TeV, 'xlab': ebeam , 'ylab': y,'leg': w_100TeV ,'ax':[-1,6,0.000000001 ,0.001], 
                    'c': 'orange' } ,
                   }


def plotter_beam(mass=''):
    fig, ax = plt.subplots(1,1)
    fnt_size = 17
    My = ''
    Mx = r'$m_ \chi$=' + mass + ' TeV'
    xpos, ypos = '',''
    if mass == '1': 
        My = r'$m_ {y0}$=2 TeV , ' + w_1TeV 
        xpos, ypos = -0.7 , 0.35
        
    elif mass == '10':
        My = r'$m_ {y0}$=20 TeV , ' + w_10TeV
        xpos, ypos = -0.7 , 0.00004
      
       
        
    elif mass == '100':
        My = r'$m_ {y0}$=200 TeV , ' + w_100TeV
        xpos, ypos = -0.7 , 0.00009
    #plt.text(xxpos, xypos , Mx , fontsize = fnt_size-3 )
    #plt.text(yxpos, yypos , My , fontsize = fnt_size-3 )
    
    
    plt.text(xpos, ypos, Mx+'\n'+My , size = fnt_size-6 , 
             va ="baseline", ha="left", multialignment="left", bbox=dict(fc="none", boxstyle ="round"), color = 'blue')
             

    plt.axis(dic_prop[mass]['ax'])
    
    plt.xlabel(dic_prop[mass]['xlab'], fontsize = fnt_size)
    plt.ylabel(dic_prop[mass]['ylab'], fontsize = fnt_size)
    plt.yscale('log')
    xl , y = dic_prop[mass]['x'] ,dic_prop[mass]['y']
    x = range(0,len(y))

    ax.set_xticks(x)
    ax.set_xticklabels(xl, minor = False, rotation= 45)
    
    print('x,y', x, y)
    plt.scatter(x, y , label = dic_prop[mass]['leg'] , color = dic_prop[mass]['c'])
    #plt.legend(loc = 'upper right', fontsize = 12)

    plt.grid(linestyle = ':')
    plt.savefig('XSEC/xsec_Ebeam_'+mass+'_TeV.png',  bbox_inches='tight')
    plt.close()
    


def plotter_singlemass(mass=''):
    fig, ax = plt.subplots(1,1)
    fnt_size = 17
    My = ''
    Mx = r'$m_ \chi$=' + mass + ' TeV'
    xpos, ypos = '',''
    if mass == '1': 
        My = r'$m_ {y0}$=2 TeV , ' + w_1TeV 
        xpos, ypos = -0.7 , 0.02
    elif mass == '10':
        My = r'$m_ {y0}$=20 TeV , ' + w_10TeV
        xpos, ypos = -0.7 , 0.00004       
    elif mass == '100':
        My = r'$m_ {y0}$=200 TeV , ' + w_100TeV
        xpos, ypos = -0.7 , 0.00009
    
    plt.text(xpos, ypos, Mx+'\n'+r'$E_{beam}=1000.1$ GeV'+'\n'+r'$X=(H,W^-,W^+,Z)$' , size = fnt_size-6 , 
             va ="baseline", ha="left", multialignment="left", bbox=dict(fc="none", boxstyle ="round"), color = 'blue')
             

    plt.axis([-1,4,0.01,100])
    
    #plt.xlabel('Process', fontsize = fnt_size)
    plt.ylabel(r'$\sigma$ [pb]', fontsize = fnt_size)
    plt.yscale('log')
    xl , y = dic_prop[mass]['x'] ,dic_prop[mass]['y']
    
    y = [48.5 , 11.86, 0.95, 0.038]
    x = range(0,len(y))
    
    for xx,yy in zip(x,y):
        plt.text(xx+0.16 , yy, str(yy) , fontsize = fnt_size-3)
        
    xl = [r'$\chi \chi \rightarrow W^-W^+$',r'$\chi \chi \rightarrow W^-W^+ X$',r'$\chi \chi \rightarrow W^-W^+ XX$',r'$\chi \chi \rightarrow W^-W^+ XXX$' ]
    ax.set_xticks(x)
    ax.set_xticklabels(xl, minor = False, rotation= 45)
    
    print('x,y', x, y)
    plt.scatter(x, y  , color = 'cyan')
    #plt.legend(loc = 'upper right', fontsize = 12)

    plt.grid(linestyle = ':')
    plt.savefig('XSEC/processes_xsec_'+mass+'_TeV.png',  bbox_inches='tight')
    plt.close()
    


    
os.system('mkdir XSEC')
a = plotter_beam(mass= '1')
a = plotter_beam(mass= '10')
a = plotter_beam(mass= '100')
a = plotter_singlemass(mass='1')
print('done with beams')    
