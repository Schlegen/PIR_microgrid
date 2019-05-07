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
		self.dt=0.5
		self.rc=0.95
		self.rd=0.95

	def compute_load(self,time): 

		return self.non_flexible(time) + self.flexible(time)
	
	def non_flexible(self,time):
		
		lp = self.scenario["load_charging_station"][time] # non flexible 
		return lp
		
	def flexible(self,time):
		
		flexible_loads = np.zeros(48)
		##To be completed by the studdents 
		
		##
		cmax = self.scenario["load_charging_station_capacity"][0,time] # Available Capacity   
		pmax = self.scenario["load_charging_station_capacity"][1,time] # Available Power
		sock = self.scenario["load_charging_station_capacity"][2,time]  # State Of Charge of the vehicle k
		
		flex_load = flexible_loads[time]
		
		l_more = (flex_load + abs(flex_load))/2  #l+
		l_less = (-flex_load + abs(flex_load))/2 #l-
		
		exciding_load=0
		if time==0:
			self.a[time]= (self.rc*l_more - 1/self.rd*l_less)*self.dt + sock 
		
		else :
			self.a[time]= slef.a[time-1] + (self.rc*l_more - 1/self.rd*l_less)*self.dt + sock 
		
		if self.a[time] > cmax :
			print ("Available energy gretter than the capacity at t= "+str(t))
			exciding_load = self.a[time]-cmax # the exciding is sailled 

			
		if self.a[time] < 0 :
			print ("Available energy lower than 0 at t= "+str(t))
			l_less = self.a[time-1]+sock
			
		if l_more+l_less > pmax :
			print (" Load gretter than the available power at t= "+str(t))
			l_more = pmax
			l_less = pmax

		flexload = l_more-l_less
		return flex_load+ execeding_load
			

	def draw_random_scenario(self):

		test_load_charging_station = np.loadtxt(os.path.join(self.path_to_data_folder, "charging-station","test_load_vehicles_charging-station.csv"))
		self.scenario["load_charging_station"]= test_load_charging_station [randint(self.n_data),:]
		
		#tableau NPY
		test_load_charging_station_capacity = np.load(os.path.join(self.path_to_data_folder, "charging-station","test_capacity_power_soc_charging-station.npy"))
		self.scenario["load_charging_station_capacity"]= test_load_charging_station_capacity [randint(self.n_data),:,:] 
