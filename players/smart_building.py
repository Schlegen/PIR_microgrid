import numpy as np
import os 
from numpy.random import randint

"""
Class for the Smart Building
Some fields must be completed by students

"""

class SmartBuilding:
    def __init__(self,path_to_data_folder):

        self.path_to_data_folder = path_to_data_folder
        self.n_data = 10
        self.dt = 0.5
        
        #données du ballon d'eau chaude
        self.e=0.4
        self.r=0.05
        self.c_p=4200
        self.rho=1
        self.V=400
        self.T_in=273+15
        self.T_com=273+60
        self.COP=(self.T_com/(self.T_com-self.T_in))*self.e

        self.max_capacity_hwt=self.rho*self.V*self.c_p*(self.T_com - self.T_in) / (3600 * 1000) # kWh !

        self.demand_curves=self.heat_demand()
        self.heat_transactions=np.zeros((48,2))

        self.scenario = {}
        self.bill = np.zeros(48)
        self.load = np.zeros(48)
        self.heat_stock=np.zeros(49)
        self.heat_stock[0]=0.25*self.max_capacity_hwt

    def heat_demand(self):
        
        demand_curves=np.zeros((48,6))
        
        ## to be completed by the students ##
        
        return demand_curves
        

    def flexible(self, time):

        hot_water_demand = self.scenario['hot_water_demand_smart-building'][time]
        heat_data_center = self.heat_transactions[time, 0]
        
        load_heat_pump = 0
        
        ## to be completed by the students ##

        return load_heat_pump


    def not_flexible(self, time):
        l_nf = self.scenario['load_smart-building'][time] 
        return l_nf

    def update_heat_stock(self, time, load_heat_pump):

        new_stock = (1-self.r)*self.heat_stock[time]+self.heat_transactions[time, 0]
        -self.scenario['hot_water_demand_smart-building'][time]+(self.COP*self.dt*load_heat_pump)

        adjustment_load = 0

        if new_stock < 0:
            adjustment_load = -new_stock / (self.COP*self.dt)
            new_stock = 0
        elif new_stock > self.max_capacity_hwt:
            new_stock = self.max_capacity_hwt
            ## no adjustment if too much power is bought: energy is wasted

        self.heat_stock[time+1] = new_stock

        return adjustment_load

    def compute_load(self, time):

        load_heat_pump = self.flexible(time)

        self.load[time] = (self.not_flexible(time) + load_heat_pump + 
            self.update_heat_stock(time, load_heat_pump))

    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_load_smart-building.csv"))
        self.scenario["load_smart-building"] = test_load_data_center[randint(self.n_data), :]
        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "smart-building","test_hot_water_demand_smart-building.csv"))
        self.scenario["hot_water_demand_smart-building"] = test_load_data_center[randint(self.n_data), :]

        self.bill = np.zeros(48)
        self.load = np.zeros(48)
        self.heat_stock=np.zeros(49)
        self.heat_stock[0]=0.25*self.max_capacity_hwt


"""
Test your code before submition

"""

if __name__ == '__main__':

    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_data = os.path.join(current_path, "..", "data")
    smart_building = SmartBuilding(path_to_data)

    if smart_building.demand_curves.shape != (48, 6):
        raise ValueError("The size of your demand curve is {}, expected size {}".format(
            smart_building.demand_curves.shape, (48, 6)))

    smart_building.draw_random_scenario()
    smart_building.compute_load(0)

    print("Test passed, ready to submit !")