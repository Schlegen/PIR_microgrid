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

        self.scenario = {}
        self.bill = np.zeros(48)
        self.load = np.zeros(48)
        self.heat_transactions = np.zeros((48,2))

        self.information={"my_buy_price" : np.zeros(49), "grid_buy_price" : np.zeros(49),
                          "my_sell_price" : np.zeros(49), "grid_sell_price" : np.zeros(49)}
                
    def heat_supply(self,t):

        supply_curves = np.zeros(6)
        mini,maxi=0,0
        if (t>=0 and t<12) or t>=44:
            maxi=0.057/1.48
            mini=0.06/2.66
        if (t>=12 and t<16) or (t>=40 and t<44):
            maxi=0.09/1.48
            mini=0.10/2.66
        if (t>=16 and t<40):
            maxi=0.08/1.48
            mini=0.1/2.66
        for q in range(6):
            supply_curves[q]=(2*q/10)*maxi+(1-2*q/10)*mini

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
        self.heat_transactions = np.zeros((48,2))


"""
Test your code before submition

"""

if __name__ == '__main__':

    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_data = os.path.join(current_path, "..", "data")
    data_center = DataCenter(path_to_data)

    data_center.draw_random_scenario()
    data_center.heat_supply(0)

    print("Test passed, ready to submit !")