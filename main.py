import numpy 
import os

from players.charging_station import ChargingStation
from players.data_center import DataCenter
from players.smart_building import SmartBuilding
from players.solar_farm import SolarFarm


class Community:

	def __init__(self, path_to_data_folder):

		self.horizon = 48
		self.dt = 0.5
		self.path_to_data_folder = path_to_data_folder

		self.players = {"charging_station": ChargingStation(path_to_data_folder), 
			"data_center": DataCenter(path_to_data_folder), 
			"smart_building": SmartBuilding(path_to_data_folder),
			"solar_farm": SolarFarm(path_to_data_folder)}

		self.initialize_prices()
		self.initialize_heat_transactions()

	def initialize_prices(self):

		prices = numpy.loadtxt(os.path.join(self.path_to_data_folder, "prices_class_1.csv"))
		self.prices = {"internal":prices[0, :], "external_purchase":prices[1, :], 
			"external_sale":prices[2, :]}

	def initialize_heat_transactions(self):
		## à compléter
		return 0

	def play(self):

		for name, player in self.players.items():
			player.draw_scenario()

		for t in range(self.horizon):

			self.call_heat(t)
			load, demand, supply = self.call_loads(t)
			self.compute_bills(t, load, demand, supply)

	def call_heat(self, time):
		LDC = self.players["data_center"].call_heat()
		LSB = self.players["smart_building"].call_heat()

		for t in range(0,48):
			q=0
			while LSB[t,q]>LDC[t,q] and q < 6:
				q+=1

		if q == 6: #no equilibrium

			eq=(qeq,peq)

		else:

			SB1, SB2 = LSB[t,q-1], LSB[t,q]
			DC1, DC2 = LDC[t,q-1], LDC[t,q]

			A = (SB1-SB2) #/1
			B = SB1[1]-A*(q-1)
			C = (DC1-DC2) #/1
			D = DC1[1]-A*(q-1)

			qeq=(D-B)/(A-C)
			peq=A*qeq+B

			eq=(qeq,peq)

		self.players["data_center"].heat_balance[time]=eq
		self.players["smart_building"].heat_balanc[time]=eq

	def call_loads(self, time):

		total_load = 0.0
		demand = 0.0
		supply = 0.0

		for name, player in self.players.items():

			player.compute_load(time)
			load = player.load[time]

			if load >= 0:
				demand += load
			else:
				supply -= load
			total_load += load

		return total_load, demand, supply

	def compute_bills(self, time, load, demand, supply):

		internal_trade = self.dt*self.prices["internal"]*min(demand, supply)

		purchase = internal_trade + self.prices["external_purchase"]*max(0, load)*self.dt
		sale = internal_trade + self.prices["external_purchase"]*max(0, -load)*self.dt

		for name, player in self.players.items():

			load = player.load[time]

			if load >= 0:
				player.bill[time] += purchase * load / demand
			else:
				player.bill[time] -= sale * load / supply