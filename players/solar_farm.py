import numpy as np
from random import randint
import os

class SolarFarm:

    def __init__(self,path_to_data_folder):
        self.scenario={}
        self.path_to_data_folder = path_to_data_folder
        self.bill = np.zeros(48)
        self.n_data = 10


    def load(self,time):

            return 0

    def draw_random_scenario(self):

        test_load_solar_farm=np.loadtxt(os.path.join(self.path_to_data_folder,"solar-farm",
                                                        "test_pv_solar-farm.csv"))
        self.scenario["load_solar_farm"]=test_load_solar_farm[randint(0,self.n_data), :]
