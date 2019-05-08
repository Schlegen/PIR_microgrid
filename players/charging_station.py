import numpy as np
import os 
from numpy.random import randint 

"""
Class for the Charging Station
Some fields must be completed by students

"""

class ChargingStation:

    def __init__(self, path_to_data_folder):

        self.path_to_data_folder = path_to_data_folder
        self.n_data = 10
        self.scenario = {}
        self.dt = 0.5

        self.bill = np.zeros(48)
        self.load = np.zeros(48)

        self.battery_stock = np.zeros(49)
        self.efficiency = 0.95

    def flexible(self,time):

        load_battery = 0
        
        ## to be completed by the students ##

        return load_battery

    def not_flexible(self,time):
        
        l_nf = self.scenario["load_charging_station"][time]
        return l_nf

    def update_batterie_stock(self, time, load_battery):

        cmax = self.scenario["load_charging_station_capacity"][0,time] # Available Capacity   
        pmax = self.scenario["load_charging_station_capacity"][1,time] # Available Power
        soc = self.scenario["load_charging_station_capacity"][2,time]  # State Of Charge of the vehicles

        if abs(load_battery) > pmax:
            load_battery = pmax*np.sign(load_battery)

        new_stock = self.battery_stock[time] + self.efficiency*load_battery*self.dt + soc

        if new_stock < 0:
            load_battery = - (self.battery_stock[time] + soc) / (self.efficiency*self.dt)
            new_stock = 0
        elif new_stock > cmax:
            load_battery = (cmax - self.battery_stock[time] - soc) / (self.efficiency*self.dt)
            new_stock = cmax

        self.battery_stock[time+1] = new_stock

        return load_battery

    def compute_load(self,time):

        load_battery = self.flexible(time)
        self.load[time] = self.not_flexible(time) + self.update_batterie_stock(time, load_battery)
            

    def draw_random_scenario(self):

        test_load_charging_station = np.loadtxt(os.path.join(self.path_to_data_folder, "charging-station","test_load_vehicles_charging-station.csv"))
        self.scenario["load_charging_station"]= test_load_charging_station [randint(self.n_data),:]
        
        #tableau NPY
        test_load_charging_station_capacity = np.load(os.path.join(self.path_to_data_folder, "charging-station","test_capacity_power_soc_charging-station.npy"))
        self.scenario["load_charging_station_capacity"]= test_load_charging_station_capacity [randint(self.n_data),:,:] 


"""
Test your code before submition

"""

if __name__ == '__main__':

    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_data = os.path.join(current_path, "..", "data")
    charging_station = ChargingStation(path_to_data)

    charging_station.draw_random_scenario()
    charging_station.compute_load(0)

    print("Test passed, ready to submit !")