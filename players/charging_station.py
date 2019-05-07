import numpy as np
import os 

from numpy.random import randint 

dt= 0.5
rc=0.95  # Charge Efficiency
rd= 0.95 # Discharge Efficiency

class ChargingStation:

	def __init__(self, path_to_data_folder):

		self.path_to_data_folder = path_to_data_folder
		self.bill = np.zeros(48)
		self.load = np.zeros(48)
		self.scenario = {}
		self.n_data = 10
		self.a=np.zeros(48)
		

	def compute_load(self,time): 

		
		return self.non_flexible(time) + self.flexible(time)
	
	def non_flexible(self,time):
		
		lp = self.scenario["load_charging_station"][time] # non flexible 
		
	def flexible(self,time):
		
		flexible_loads = np.zeros(48)
		##To be completed by the studdents 
		
		##


		cmax = self.scenario["load_charging_station_capacity"][0][time] # Available Capacity   
		pmax = self.scenario["load_charging_station_capacity"][1][time] # Available Power 
		sock = self.scenario["load_charging_station_capacity"][2][time]  # State Of Charge of the vehicle k
		
		flex_load = flexible_loads[time]
		
		l_more = (flex_load + abs(flex_load))/2  #l+
		l_less = (-flex_load + abs(flex_load))/2 #l-
		
		if time==0:
			self.a[time]= (rc*l_more - 1/rd*l_less)*dt + sock 
		
		else :
			self.a[time]= slef.a[time-1] + (rc*l_more - 1/rd*l_less)*dt + soc 
		
		if self.a[time] > cmax :
			print ("Available energy gretter than the capacity at t= "+str(t))
			
		if self.a[time] < 0 :
			print ("Available energy lower than 0 at t= "+str(t))
			
		if l_more+l_less > pmax :
			print (" Load gretter than the available power at t= "+str(t))
			
			
		return flex_load
			

	def draw_random_scenario(self):
		n = randint(self.n_data)
		
		test_load_charging_station = np.loadtxt(os.path.join(self.path_to_data_folder, "charging-station","test_load_vehicles_charging-station.csv"))
		self.scenario["load_charging_station"]= test_load_charging_station [n,:]
		
		#tableau NPY
		test_load_charging_station_capacity = np.load(os.path.join(self.path_to_data_folder, "charging-station","test_capacity_power_soc_charging-station.npy"))
		self.scenario["load_charging_station_capacity"]= test_load_charging_station_capacity [n,:,:] 
		
		return 0