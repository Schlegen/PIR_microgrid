# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:37:58 2019

@author: FNAC4008
"""

## différents types de call
                    
def gaussiancall(t,avg,sigma,maxi): return(maxi*(mh.e**(-((t-avg)**2)/(2*sigma**2)))/2*mh.sqrt(2*mh.pi))  
def squarecall(t, inf, sup, maxi): 
    if ((t>=inf) and (t<sup)): 
        return maxi 
    else:
        return 0
def randomcall(t,avg, sigma):
    return(0.+avg+randint(-sigma,sigma))

        
callfunctions={"building": (lambda t: squarecall(t,8,18,10)) , "data_center": (lambda t: randomcall(t,7,3)), "PV_production": (lambda t:gaussiancall(t,12,2,-16)),"VE": (lambda t: randomcall(t,0,5))   }        
names=[ "building", "data_center", "PV_production", "VE"]
manager=Manager(names,callfunctions)        
manager.simulation(24)        
app = SummaryWindow(manager)
app.mainloop()    