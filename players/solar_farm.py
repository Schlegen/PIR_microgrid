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
        self.capacity =100
        self.efficiency=0.95
        self.overload=70
        self.timestep=0.5
        self.load=np.zeros(48)
    
    
    def compute_load(self,time):

            self.load[time] = self.flexible(time)+self.not_flexible(time)
    
    def flexible(self,time):
        return(0)
        
    def not_flexible(self,time):
        limitation = 0
        charge=self.flexible(time)
        if charge > self.overload:
            limitation = self.overload-charge
            charge=self.overload
        if charge < -self.overload:
            limitation = -self.overload-charge
            charge=-self.overload
        if charge > 0:
            available_charge=self.capacity-self.charge[time-1]
            if self.efficiency*charge*self.timestep < available_charge:
                self.charge[time] = self.charge[time-1] + self.efficiency*charge*self.timestep
                charge=0
            else:
                charge = charge-(available_charge/(self.efficiency*self.timestep))
                self.charge[time]=self.capacity
        if charge < 0:
            available_charge = self.charge[time-1]
            if -charge*self.timestep/self.efficiency < available_charge:
                self.charge[time] = available_charge + charge*self.timestep/self.efficiency
                charge=0
            else:
                charge = charge+(available_charge*self.efficiency/self.timestep)
                self.charge[time]=0
        return(-self.scenario["load_solar_farm"][time]-charge+limitation)
    
    def draw_random_scenario(self):

        test_load_solar_farm=np.loadtxt(os.path.join(self.path_to_data_folder,"solar-farm",
                                                        "test_pv_solar-farm.csv"))
        self.scenario["load_solar_farm"]=test_load_solar_farm[randint(0,self.n_data), :]
