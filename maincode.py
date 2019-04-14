import numpy as np
from random import randint
import math as mh

class Player:  
    def __init__(self,load,bill,callfunction,supplied,name):
        self.load = load # négatif si on produit
        self.bill =  bill # positif si on produit
        self.callfunction = callfunction
        self.supplied =supplied
        self.name=name
    def call(self, t):
        self.load.append(self.callfunction(t+.5))              
class Manager:
    def __init__(self, names, callfunctions):
        self.names = names
        self.callfunctions = callfunctions
        dictionnary_players={}
        for name in names:
           dictionnary_players[name]=Player([],[], callfunctions[name],[],name)         
        self.players = dictionnary_players        
        self.pe = 1.
        self.c = 0.5
        self.v= 2.
        self.loads = []
        self.production = []
        self.balance = []
        self.max_power= 12
        
    def repartition(self):
        if abs(self.loads[-1])>self.max_power : #on dépasse l'intensité maximale possible
            for name in self.names:
                player = self.players[name]
                if player.load[-1]>0 : #consommateur, dont on restreind l'énergie accessible
                    player.supplied.append(player.load[-1]*(1-(self.max_power+self.loads[-1])/self.loads[-1])) #on réparti le manque proportionellement aux demandes 
                else : #producteur, dont on garde la production maximale pour minimiser les coûts
                    player.supplied.append(player.load[-1])

        else : #RAS, la demande égale à ce que le réseau peut fournir
            for name in self.names:
                player = self.players[name]
                player.supplied.append(player.load[-1])
        
        if self.balance[-1] > 0: #on exporte
            for name in self.names:
                player = self.players[name]
                if player.load[-1] <0. : #pour les producteurs bill postive
                    player.bill.append( (-player.supplied[-1]/self.production[-1])*(-self.loads[-1]*self.pe+self.balance[-1]*self.c) ) #car self.loads est négatif
                else: # pour les consommateurs bill negative
                    player.bill.append( -player.supplied[-1]*self.pe )  #negatif car self.loads negatif
        else: #on importe 
            for name in self.names:
                player = self.players[name]
                if player.load[-1] <0. : #pour les producteurs bill positive
                    player.bill.append( (-player.supplied[-1]*self.pe ) )
                else: # pour les consommateurs bill négative
                    player.bill.append( (player.supplied[-1]/self.loads[-1])*(self.production[-1]*self.pe-self.balance[-1]*self.v) ) # car le balance est négatif
        
    def simulation(self, T):
        for t in range(T):
            self.loads.append(0)
            self.production.append(0)   
            for name in self.names:
                player = self.players[name]   
                player.call(t)   
                if player.load[-1]>0:
                    self.loads[-1]+= -player.load[-1] #demande negative
                else:
                    self.production[-1] += -player.load[-1] #production positive
            self.balance.append( self.production[-1]+self.loads[-1]) #positif si on exporte et négatif sinon   
            self.repartition()

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