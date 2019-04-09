import numpy as np
import matplotlib.pyplot as plt
from random import randint
import math as mh
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

class Player:
    def __init__(self,load,bill,callfunction):
        self.load = load # négatif si on produit
        self.bill =  bill # positif si on produit
        self.callfunction = callfunction
        
    def call(self, t):
        self.load.append(self.callfunction(t+.5))
        
    def plotload(self):
        fig, ax = plt.subplots(1)
        rects=[]
        for t in range(len(self.load)):
            rect= Rectangle( (t,0),1,self.load[t] )
            rects.append(rect)
        # Create patch collection with specified colour/alpha
        pc = PatchCollection(rects, alpha=0.5, facecolor="grey", edgecolor="black")
        # Add collection to axes
        ax.add_collection(pc)
        ax.set_xlim(0,len(self.load))
        ax.set_ylim(1.2*min(0,min(self.load)),1.2*max(self.load))
        ax.grid(True)
        
    def plotbills(self):
        fig, ax = plt.subplots(1)
        rects=[]
        for t in range(len(self.load)):
            rect= Rectangle( (t,0), 1, self.bill[t] )
            rects.append(rect)
        # Create patch collection with specified colour/alpha
        pc = PatchCollection(rects, alpha=0.5, facecolor="green", edgecolor="black")
        # Add collection to axes
        ax.add_collection(pc)
        ax.set_xlim(0,len(self.load))
        ax.set_ylim(1.2*min(0,min(self.bill)),1.2*max(0,max(self.bill)))
        ax.grid(True)
        
class Manager:
    def __init__(self, names, callfunctions):
        self.names = names
        self.callfunctions = callfunctions
        dictionnary_players={}
        for name in names:
           dictionnary_players[name]=Player([],[], callfunctions[name])         
        self.players = dictionnary_players        
        self.pe = 1.
        self.c = 0.5
        self.v= 2.
        self.loads = []
        self.production = []
        self.balance = []
        
    def repartition(self):
        if self.balance[-1] > 0: #on exporte
            for name in self.names:
                player = self.players[name]
                if player.load[-1] <0. : #pour les producteurs bill postive
                    player.bill.append( (-player.load[-1]/self.production[-1])*(-self.loads[-1]*self.pe+self.balance[-1]*self.c) ) #car self.loads est négatif
                else: # pour les consommateurs bill negative
                    player.bill.append( -player.load[-1]*self.pe )  #negatif car self.loads negatif
        else: #on importe 
#warning: (faire attention au max)
            for name in self.names:
                player = self.players[name]
                if player.load[-1] <0. : #pour les producteurs bill positive
                    player.bill.append( (-player.load[-1]*self.pe ) )
                else: # pour les consommateurs bill négative
                    player.bill.append( (player.load[-1]/self.loads[-1])*(self.production[-1]*self.pe-self.balance[-1]*self.v) ) # car le balance est négatif              
    
    def plotbalance(self):                         
        fig, ax = plt.subplots(1)
        rects=[]
        for t in range(len(self.balance)):
            rect= Rectangle( (t,0), 1, self.balance[t] )
            rects.append(rect)
        # Create patch collection with specified colour/alpha
        pc = PatchCollection(rects, alpha=0.5, facecolor="orange", edgecolor="black")
        # Add collection to axes
        ax.add_collection(pc)
        ax.set_xlim(0,len(self.balance))
        ax.set_ylim(1.2*min(0,min(self.balance)),1.2*max(0,max(self.balance)))
        ax.grid(True)
        
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
        print("\n Total load =")#, self.loads, "\n balance =", self.balance)
        self.plotbalance()
        plt.show()
        for name in self.names:
            player = self.players[name]
            print("\n", name)#, "\n load =", player.load, "\n bill =", player.bill)
            player.plotload()
            plt.show()
            player.plotbills()
            plt.show()
            
    
        
                    
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