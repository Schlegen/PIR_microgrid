import numpy as np
import os 
from numpy.random import randint

class SmartBuilding:
    def __init__(self,path_to_data_folder):#fichier data
        self.path_to_data_folder = path_to_data_folder
        self.bill = np.zeros(48)
        self.n_data = 10
        self.scenario={}
        self.stock=np.zeros(49)
        self.load=np.zeros(48)
        self.heat_balance=np.zeros(48)
        
        #données du ballon d'eau chaude
        self.e=0.4
        self.r=0.05
        self.c_p=4200
        self.rho=1
        self.V=400
        self.T_in=273+15
        self.T_com=273+60
        self.COP=(self.T_com/(self.T_com-self.T_in))*self.e
        self.delta_t=3600/2
        self.stock[0]=0.25*self.rho*self.V*self.c_p*(self.T_com - self.T_in)

    def compute_load(self, time):
        self.load[time]=self.not_flexible(time) + self.flexible(time) 

    def call_heat(self):
        
        prices=np.zeros((48,6))
        
        #mettre prices à jour avec le prix unitaire du kW/h aux quantitées : 0;0,2;0,4;0,6;0,8;1 de q_max
        
        
        return(prices)
        

    def flexible(self, time):
        
        #on demande une certaine énergie pour chauffer le ballon
        
        thermal_load=0
        
        return (thermal_load) #énergie demandée pour chauffer le ballon


    def not_flexible(self, time):
        
        load=0
        
        load+=self.scenario['load_smart-building'][t] #demande en énergie domestique
        
        #Evolution du stock d'eau chaude:
        stock[time+1]=(1-self.r)*stock[time]+heat_balance[time]-self.scenario['hot_water_demand_smart-building'][t]+(self.COP*self.detla_t*flexible(self,time,heat_exchange))
        
        if (stock[time+1]<0):#on s'assure qu'il y ait assez d'eau chaude
            load+=(-self.stock[times+1]/(self.delta_t*self.COP))
            stock[time+1]=0
        return load


    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_load_smart-building.csv"))
        self.scenario["load_smart-building"] = test_load_data_center[randint(self.n_data), :]
        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_hot_water_demand_smart-building.csv"))
        self.scenario["hot_water_demand_smart-building"] = test_load_data_center[randint(self.n_data), :]