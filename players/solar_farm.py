import numpy as np
import os
from numpy.random import randint

"""
Class for the Solar Farm
Some fields must be completed by students

"""

class SolarFarm:

    def __init__(self,path_to_data_folder):

        self.path_to_data_folder = path_to_data_folder
        self.n_data = 10
        self.dt = 0.5

        self.capacity =100
        self.efficiency=0.95
        self.max_load=70

        self.scenario = {}
        self.bill = np.zeros(48)
        self.load = np.zeros(48)
        self.battery_stock = np.zeros(49)
        
        self.information={"my_buy_price" : np.zeros(49), "grid_buy_price" : np.zeros(49),
                          "my_sell_price" : np.zeros(49), "grid_sell_price" : np.zeros(49)}

    def flexible(self,time):

        load_battery = 0
        stock = self.battery_stock[time]
        solar_power = self.scenario["load_solar_farm"][time]

        if time < 12 :
            load_battery = 17
            
        if (time >11 and time < 17 and self.information["grid_buy_price"][time]<= 0.09):
            load_battery = -25
        if (time >11 and time < 17 and self.information["grid_buy_price"][time]> 0.09):
            load_battery = -max(1/5*stock,25)
        
        if (time >16 and time < 23 and self.information["grid_buy_price"][time]<= 0.08):
            load_battery = -15
        if (time >16 and time < 23 and self.information["grid_buy_price"][time]> 0.08):
            load_battery = -max(1/5*stock,15)

        if(time>22 and time <25 and self.information["grid_buy_price"][time]<= 0.08):
            load_battery = -15
        if(time>22 and time <25 and self.information["grid_buy_price"][time]> 0.08):
            load_battery = -max(1/5*stock,15)
            
        if self.scenario["load_solar_farm"][23]>30:#kW
            if(time > 24 and time< 30):
                load_battery = 30
        if self.scenario["load_solar_farm"][23]<=30:#kW
            if(time > 24 and time< 30):
                load_battery = 15
    
        if  time > 29 and time < 38 :
                load_battery = - 1/5*stock
        
        if (time > 37 and time < 41 and self.information["grid_buy_price"][time]<= 0.08):
                load_battery = -60
        if (time > 37 and time < 41 and self.information["grid_buy_price"][time]> 0.08):
                load_battery = -max(1/5*stock,60)
        
        if (time > 40) :
                load_battery = -2*self.battery_stock[41]/6

        return load_battery

    def not_flexible(self, time):
        return -self.scenario["load_solar_farm"][time]

    def update_batterie_stock(self, time, load_battery):

        if abs(load_battery) > self.max_load:
            load_battery = self.max_load*np.sign(load_battery)

        new_stock = self.battery_stock[time] + self.efficiency*load_battery*self.dt

        if new_stock < 0:
            load_battery = - self.battery_stock[time] / (self.efficiency*self.dt)
            new_stock = 0
        elif new_stock > self.capacity:
            load_battery = (self.capacity - self.battery_stock[time]) / (self.efficiency*self.dt)
            new_stock = self.capacity

        self.battery_stock[time+1] = new_stock

        return load_battery

    def compute_load(self,time):

        load_battery = self.flexible(time)
        self.load[time] = self.not_flexible(time) + self.update_batterie_stock(time, load_battery)
    
    def draw_random_scenario(self):

        test_load_solar_farm=np.loadtxt(os.path.join(self.path_to_data_folder,"solar-farm",
                                                        "test_pv_solar-farm.csv"))
        self.scenario["load_solar_farm"]=test_load_solar_farm[randint(0,self.n_data), :]

        self.bill = np.zeros(48)
        self.load = np.zeros(48)
        self.battery_stock = np.zeros(49)


"""
Test your code before submition

"""

if __name__ == '__main__':

    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_data = os.path.join(current_path, "..", "data")
    solar_farm = SolarFarm(path_to_data)

    solar_farm.draw_random_scenario()
    solar_farm.compute_load(0)
    for i in range(48):
        solar_farm.flexible(i)

    print("Test passed, ready to submit !")