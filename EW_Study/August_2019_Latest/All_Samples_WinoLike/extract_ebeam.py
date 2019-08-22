import os,sys



l = '#  Integrated weight (pb)  :       10.76031' 

ff=  'ebeam1'

b = 'w'
for f in [ f for f in os.listdir('.') if '.lhe' in f and b in f ]:
    l = open(f, 'r').readlines()[1:200]
    for m in l:
        if ff in m:
            print(f , '_', m )          


            
