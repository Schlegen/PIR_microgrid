import numpy as np
import os 
from numpy.random import randint

class SmartBuilding:
    def __init__(self,path_to_data_folder):#fichier data, truc spécifique
        self.path_to_data_folder = path_to_data_folder
        self.bill = np.zeros(48)
        self.n_data = 10
        self.scenario={}
        
        self.load=np.zeros(48)

    def load(self, time):
        return self.not_flexible(time) + self.flexible(time) 

    def not_flexible(self, time):

        return 0 

    def flexible(self, time):

        return 0

    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_load_smart-building.csv"))
        self.scenario["load_smart-building"] = test_load_data_center[randint(self.n_data), :]
        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_hot_water_demand_smart-building.csv"))
        self.scenario["hot_water_demand_smart-building"] = test_load_data_center[randint(self.n_data), :]