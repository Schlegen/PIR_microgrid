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
        self.heat_balance=np.zeros((48,2))
        self.demand_curves=self.thermic_demand()
        
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

        self.max_capacity_hwt=self.rho*self.V*self.c_p*(self.T_com - self.T_in)
        self.stock[0]=0.25*self.max_capacity_hwt

    def compute_load(self, time):
        self.load[time]=self.not_flexible(time) + self.flexible(time) 

    def thermic_demand(self):
        
        demand_curves=np.zeros((48,6))
        
        #to be completed by the students
        
        
        return demand_curves
        

    def flexible(self, time):
        
        #To be completed : electric power required to heat the water tank
        
        load_h=0
        

        return load_h 


    def not_flexible(self, time):
        
        load = self.scenario['load_smart-building'][time] #houshold power demand
        
        #Evolution of the hot water tank
        stock[time+1] = (1-self.r)*stock[time]+heat_balance[time][0]
        -self.scenario['hot_water_demand_smart-building'][time]+
        (self.COP*self.detla_t*self.flexible(time))
        
        if (stock[time+1]<0):#if there isn't enough hot water
            load+=(-self.stock[time+1]/(self.delta_t*self.COP)) #the required power is bought anyway
            stock[time+1] = 0

        if stock[time+1]>self.max_capacity_hwt:
            stock[time+1] = self.max_capacity_hwt

        return load


    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_load_smart-building.csv"))
        self.scenario["load_smart-building"] = test_load_data_center[randint(self.n_data), :]
        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_hot_water_demand_smart-building.csv"))
        self.scenario["hot_water_demand_smart-building"] = test_load_data_center[randint(self.n_data), :]