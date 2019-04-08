import numpy as np
import matplotlib.pyplot as plt
from random import randint


class Player:
    def __init__(self,load,bill):
        self.load = load # négatif si on produit
        self.bill =  bill # positif si on produit
    def call(self, t):
        self.load.append(randint(-10,10))
        
class Manager:
    def __init__(self, names):
        self.names = names
        dictionnary_players={}
        for name in names:
           dictionnary_players[name]=Player([],[])         
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
                    player.bill.append( player.load[-1]*self.pe )  #negatif car self.loads negatif
        else: #on importe 
#warning: (faire attention au max)
            for name in self.names:
                player = self.players[name]
                if player.load[-1] <0. : #pour les producteurs bill positive
                    player.bill.append( (player.load[-1]/self.production[-1])*self.loads[-1]*self.pe )
                else: # pour les consommateurs bill négative
                    player.bill.append( (player.load[-1]/self.loads[-1])*(self.production[-1]*self.pe-self.balance[-1]*self.v) ) # car le balance est négatif              
                              
            
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
            
        print("\n Total load =", self.loads, "\n balance =", self.balance)    
        for name in self.names:
            player = self.players[name]
            print("\n", name, "\n load =", player.load, "\n bill =", player.bill)

            

names=[ "building", "data_center"] #, "PV_production", "VE"]

manager=Manager(names)        
        
manager.simulation(1)       
        
        
        
        
        
        
        