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
		self.dt = 0.5

		self.efficiency = 0.95

		self.scenario = {}
		self.bill = np.zeros(48)
		self.load = np.zeros(48)
		self.battery_stock = {"slow" : np.zeros(48), "fast" : np.zeros(48)}
		
		self.information={"my_buy_price" : np.zeros(48), "grid_buy_price" : np.zeros(48),
                          "my_sell_price" : np.zeros(48), "grid_sell_price" : np.zeros(48)}

	def flexible(self,time):
		load_battery = {"slow" : 0, "fast" : 0}
		my_buy_price = self.information["my_buy_price"][t]
		my_sell_price = self.information["my_sell_price"][t]
		grid_buy_price = self.information["grid_buy_price"][t]
		grid_sell_price = self.information["my_sell_price"][t]
		
		pmax = self.scenario["load_charging_station_capacity"][1,time]
		soc = self.scenario["load_charging_station_capacity"][2,time]
		## to be modified
		if time<12:
			load_battery = pmax
		elif time<18 :
			load_battery = -pmax
		if time> 30 :
			load_battery = -soc
			
		return load_battery


	def update_batterie_stock(self, time, load_battery):
		
		cmax = self.scenario["load_charging_station_capacity"][0,time] # Available Capacity   
		pmax = self.scenario["load_charging_station_capacity"][1,time] # Available Power
		soc = self.scenario["load_charging_station_capacity"][2,time]  # State Of Charge of the vehicles
		
		nb_slow = int((pmax%22)/3)   # nombre de voiture à 3kW dispo 
		nb_fast = cmax/40 - nb.slow # nombre de voiture à 22kW dispo 
		nb={"slow" : nb_slow, "fast" : nb_fast}
		pmax = {"slow" : 3*nb_slow, "fast" : 22*nb_fast}
		cmax = {"slow" : 40*nb_slow, "fast" : 40*nb_fast}
		
		for speed in ["slow","fast"] :
			if abs(load_battery[speed]) > pmax[speed] :
				load_battery[speed] = pmax[speed]*np.sign(load_battery[speed])

			new_stock = { "slow" : self.battery_stock[time] + (self.efficiency*max(0,load_battery["slow"])-min(0,load_battery["slow"])/self.efficiency)*self.dt + soc, "fast" : self.battery_stock[time] + (self.efficiency*max(0,load_battery["fast"])-min(0,load_battery["fast"])/self.efficiency)*self.dt }

		for speed in ["slow","fast"] :
			if new_stock[speed] < 0:
				load_battery[speed] = min(pmax[speed], - (self.battery_stock[speed][time] + soc)*self.efficiency/self.dt)
				new_stock[speed] = self.battery_stock[time] + (load_battery[speed]/self.efficiency)*self.dt + soc
	
			elif new_stock[speed] > cmax[speed]:
				load_battery[speed] = max(pmax[speed],(cmax[speed]*self.dt - self.battery_stock[speed][time] - soc) * self.efficiency/self.dt)
				new_stock[speed] = cmax[speed]

		if time>12 and time<18:
			speed = "slow"
			if nb[speed]*10 > new_stock[speed] :
					self.bill[time] += 1
			
			speed="fast"
			if nb[speed]*10 > new_stock[speed] :
				load_battery[speed]=nb[speed]*22
				new_stock[speed]+= 22*nb[speed]*self.dt
		
		for speed in ["slow","fast"] :
			self.battery_stock[speed][time+1] = new_stock[speed]
		
		return load_battery
		


	def compute_load(self,time):

		load_battery = self.flexible(time)
		load = self.update_batterie_stock(time, load_battery)
		self.load[time] = load["slow"] + load[fast]


	def draw_random_scenario(self):

		test_load_charging_station = np.loadtxt(os.path.join(self.path_to_data_folder, "charging-station","test_load_vehicles_charging-station.csv"))
		self.scenario["load_charging_station"]= test_load_charging_station [randint(self.n_data),:]

		#tableau NPY
		test_load_charging_station_capacity = np.load(os.path.join(self.path_to_data_folder, "charging-station","test_capacity_power_soc_charging-station.npy"))
		self.scenario["load_charging_station_capacity"]= test_load_charging_station_capacity [randint(self.n_data),:,:] 

		self.bill = np.zeros(48)
		self.load = np.zeros(48)
		self.battery_stock = np.zeros(49)


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