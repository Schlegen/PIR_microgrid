import numpy as np
import os 

from numpy.random import randint 
class ChargingStation:

	def __init__(self, path_to_data_folder):

		self.path_to_data_folder = path_to_data_folder
		self.bill = np.zeros(48)
		self.scenario = {}
		self.n_data = 10


	def load(self,time):

		return 0

	def draw_random_scenario(self):
		test_load_charging_station =np.loadtxt(os.path.join(self.path_to_data_folder, "charging-station","test_load_vehicles_charging-station.csv"))
		self.scenario["load_charging_station"]= test_load_charging_station [randint(self.n_data),:]
		
		#tableau NPY
		test_load_charging_station_capacity =np.load(os.path.join(self.path_to_data_folder, "charging-station","test_capacity_power_soc_charging-station.npy"))
		self.scenario["load_charging_station_capacity"]= test_load_charging_station_capacity [randint(self.n_data),:,:] 
		
		return 0