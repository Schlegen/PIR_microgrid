import numpy as np
from random import randint
import os

class SolarFarm:

    def __init__(self,path_to_data_folder):
        self.scenario={}
        self.path_to_data_folder = path_to_data_folder
        self.bill = np.zeros(48)
        self.n_data = 10
        self.charge=np.zeros(48)
        self.capacite=100
        self.efficiency=0.95
        self.overload=35
    def load(self,time):

            return self.flexible(time)+self.not_flexible(time)
    
    def flexible(self,time):
        return(10)
        
    def not_flexible(self,time):
        charge=self.flexible(time)
        if charge>
        if charge > 0:
            available_charge=self.capacite-self.charge[time-1]
            if self.efficiency*charge < available_charge:
                self.charge[time] = self.charge[time-1] + self.efficiency*charge/2
                charge=0
            else:
                charge = charge-(available_charge/self.efficiency)
                self.charge[time]=self.capacite
        if self.flexible(time) < 0:
            available_charge = self.charge[time-1]
            if -charge/self.efficiency < available_charge:
                self.charge[time] = available_charge + charge/self.efficiency
                charge=0
            else:
                charge = charge+(available_charge*self.efficiency)
                self.charge[time]=0
        return(-self.scenario["load_solar_farm"][time]-charge)
    
    def draw_random_scenario(self):

        test_load_solar_farm=np.loadtxt(os.path.join(self.path_to_data_folder,"solar-farm",
                                                        "test_pv_solar-farm.csv"))
        self.scenario["load_solar_farm"]=test_load_solar_farm[randint(0,self.n_data), :]
