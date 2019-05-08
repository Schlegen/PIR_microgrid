import numpy as np
import os
from numpy.random import randint


"""
Class for the Data Center
Some fields must be completed by students

"""

class DataCenter:

    def __init__(self, path_to_data_folder):

        self.path_to_data_folder = path_to_data_folder
        self.n_data = 10
        self.dt = 0.5

        self.EER = 4
        self.COP = self.EER + 1
        self.COP_HP=0.4*(273+60)/(60-35)

        self.supply_curves = self.heat_supply()
        self.heat_transactions = np.zeros((48,2))

        self.scenario = {}
        self.bill = np.zeros(48)
        self.load = np.zeros(48)
                
    def heat_supply(self):
        
        supply_curves = np.zeros((48,6))

        ## to be completed by the students ##

        return supply_curves
        
    def flexible(self,time):
        l_hp = self.heat_transactions[time][0]/(self.COP_HP*self.dt)
        return l_hp
        
    def not_flexible(self,time):
        l_it = self.scenario["load_data_center"][time]
        h_it = l_it 
        l_cs = h_it/(self.dt*self.EER)
        return l_it + l_cs
        
    def compute_load(self,time): 
        self.load[time] = self.flexible(time)+self.not_flexible(time)
    
    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "data-center",
                                                        "test_load_data-center.csv"))
        self.scenario["load_data_center"] = test_load_data_center[randint(self.n_data), :]

        self.bill = np.zeros(48)
        self.load = np.zeros(48)


"""
Test your code before submition

"""

if __name__ == '__main__':

    current_path = os.path.realpath(__file__)
    path_to_data = os.path.join(current_path, "..", "data")
    data_center = DataCenter(path_to_data)

    if data_center.supply_curves.shape != (48, 6):
        raise ValueError("The size of your supply curve is {}, expected size {}".format(
            data_center.supply_curves.shape, (48, 6)))

    print("Test passed, ready to submit !")