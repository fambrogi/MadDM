import os,sys


index = 900
l = '#  Integrated weight (pb)  :       10.76031' 



b = 'wx'
for f in [ f for f in os.listdir('.') if '.lhe' in f and b in f ]:
    l = open(f, 'r').readlines()[850:950]
    for m in l:
        if '#  Integrated weight (pb)  :' in m:
            xsec = m.split(':')[1]
            print(f, '_', xsec )



            
