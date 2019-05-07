import numpy as np
import os
from numpy.random import randint

class DataCenter:

    def __init__(self, path_to_data_folder):

        self.path_to_data_folder = path_to_data_folder
        self.bill = np.zeros(48)
        self.n_data = 10
        self.scenario = {}
        self.dt = 0.5
        self.EER = 4
        self.COP = self.EER + 1
        self.heat_balance = np.zeros(48)
        self.load = np.zeros(48)
        
    def thermic_supply(self):
        
        prices= np.zeros((48,6)
        # to complete
        return(prices)
        
    def flexible(self,time):
        lHP = 0
        if self.heat_balance[time][0] > 0:
            LHP=1
        return(0)
        
    def not_flexible(self,time):
        lIT = self.scenario["load_data_center"][t]
        hIT = lIT 
        lCS = hIT/(self.dt*self.EER)
        return(0)
        
    def compute_load(self,time): #not_flexible
        self.load[time]=self.flexible(time)+self.not_flexible(time)
    
    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "data-center",
                                                        "test_load_data-center.csv"))
        self.scenario["load_data_center"] = test_load_data_center[randint(self.n_data), :]

