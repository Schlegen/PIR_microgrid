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

        self.scenario = {}
        self.bill = np.zeros(48)
        self.load = np.zeros(48)
        self.heat_transactions = np.zeros((48,2))
        self.heat_stock=np.zeros(49)
        self.heat_stock[0]=0.25*self.max_capacity_hwt
        self.information={"my_buy_price" : np.zeros(49), "grid_buy_price" : np.zeros(49),
                          "my_sell_price" : np.zeros(49), "grid_sell_price" : np.zeros(49)}

    def heat_demand(self,time):
        
        ## to be completed by the students ##
        demand_curve = np.zeros(6)
        heat_stock = self.heat_stock[time]
        hwt_cap  = self.max_capacity_hwt
        
        Watt_max_achat = hwt_cap - heat_stock
        
        if time < 12:
            min = (0.06/2.66)
            max = 0.057/1.48
             
                    
        if time<16 and time >=12:
            min=0.1/2.66
            max=0.09/1.48
        
        if time<39 and time >=16:
            min=0.1/2.66
            max=0.08/1.48
            
            
        else:
            min=max=0
        
        if Watt_max_achat >= 10:
                
                for i in range(6):
                    demand_curve[i]=max - i * (max -min)/5
            else:
                for i in range(Watt_max_achat//2):
                    demand_curve[i]=max - i * (max -min)/5
                for i in range((Watt_max_achat//2)+1,6,1):
                    demand_curve[i]=0
        
        
        return demand_curve


    def flexible(self, time):

        hot_water_demand = self.scenario['hot_water_demand_smart-building'][time]
        heat_stock = self.heat_stock[time]
        heat_data_center = self.heat_transactions[time, 0]
        
        
        buy_price = self.information["my_buy_price"][time]
        grid_buy_price = self.information["grid_buy_price"][time]
        
        load_heat_pump = 0
        
        
        ## to be completed by the students ##
        if 4<=time and time<=6: 
            load_heat_pump = 7
            if heat_stock+heat_data_center > self.max_capacity_hwt-7:
                 load_heat_pump=self.max_capacity_htw-heat_stock-heat_data_center

        if 9<=time and time<=11:
            load_heat_pump = 1
            if buy_price>=0.08:
                load_heat_pump = 0
            if heat_stock==heat_data_center >= self.max_capacity_hwt:
                load_heat_pump=0
        if time>=12:
            load_heat_pump=0
           
        
        

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
        self.heat_transactions = np.zeros((48,2))
        self.heat_stock=np.zeros(49)
        self.heat_stock[0]=0.25*self.max_capacity_hwt


"""
Test your code before submition

"""

if __name__ == '__main__':

    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_data = os.path.join(current_path, "..", "data")
    smart_building = SmartBuilding(path_to_data)

    smart_building.draw_random_scenario()
    smart_building.compute_load(0)
    smart_building.heat_demand(0)

    print("Test passed, ready to submit !")