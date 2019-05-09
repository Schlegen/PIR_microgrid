import numpy 
import os
import argparse

from players.charging_station import ChargingStation
from players.data_center import DataCenter
from players.smart_building import SmartBuilding
from players.solar_farm import SolarFarm
from players.solar_farm_2 import SolarFarm2



class Community:

	def __init__(self, path_to_data_folder):

		self.horizon = 48
		self.dt = 0.5
		self.path_to_data_folder = path_to_data_folder

		self.players = {"charging_station": ChargingStation(path_to_data_folder), 
			"data_center": DataCenter(path_to_data_folder), 
			"smart_building": SmartBuilding(path_to_data_folder),
			"solar_farm": SolarFarm(path_to_data_folder),
			"solar_farm_2": SolarFarm2(path_to_data_folder)}

		self.initialize_prices()
		self.initialize_heat_transactions()

	def initialize_prices(self):

		prices = numpy.loadtxt(os.path.join(self.path_to_data_folder, "prices_class_1.csv"))
		self.prices = {"internal":prices[0, :], "external_purchase":prices[1, :], 
			"external_sale":prices[2, :]}

	def initialize_heat_transactions(self):

		q_dc = self.players["data_center"].supply_curves
		q_sb = self.players["smart_building"].demand_curves

		for t in range(48):
			q = 0
			while q_sb[t,q] >= q_dc[t,q]:
				q+=1
				if q == 6:
					break

			if q == 6: #no equilibrium

				eq = [0,0]

			else:

				sb1, sb2 = q_sb[t,q-1], q_sb[t,q]
				dc1, dc2 = q_dc[t,q-1], q_dc[t,q]

				A = (sb2-sb1) / 2 #dy/dx
				B = sb1-A*(q-1)*2
				C = (dc2-dc1) / 2 #dy/dx
				D = dc1-C*(q-1)*2

				qeq = (D-B)/(A-C)
				peq = A*qeq+B

				eq = [qeq,peq]

			self.players["data_center"].heat_transactions[t] = eq
			self.players["smart_building"].heat_transactions[t] = eq

	def play(self):

		for name, player in self.players.items():
			player.draw_random_scenario()

		for t in range(self.horizon):

			load, demand, supply = self.call_loads(t)
			self.compute_electricity_bills(t, load, demand, supply)
			self.compute_heat_bills(t)

	def simulate(self, path_to_save_folder, n=1000):

		loads = numpy.zeros((5, n, 48))
		bills = numpy.zeros((5, n, 48))
		stocks = numpy.zeros((4, n, 49))
		heat_transactions = numpy.zeros((2, 1, 48))

		keys = {"charging_station": 0, 
			"data_center": 1, 
			"smart_building": 2,
			"solar_farm": 3,
			"solar_farm_2": 4}

		for i in range(n):

			self.play()

			for name, player in self.players.items():
				j = keys[name]
				loads[j, i, :] = player.load
				bills[j, i, :] = player.bill
				if name == "charging_station":
					stocks[0, i, :] = player.battery_stock
				elif name == "smart_building":
					stocks[1, i, :] = player.heat_stock
				elif name == "solar_farm":
					stocks[2, i, :] = player.battery_stock
				elif name == "solar_farm_2":
					stocks[3, i, :] = player.battery_stock
				j += 1

		numpy.save(os.path.join(path_to_save_folder, "load"), loads)
		numpy.save(os.path.join(path_to_save_folder, "bill"), bills)
		numpy.save(os.path.join(path_to_save_folder, "stock"), stocks)

		heat_transactions = self.players["smart_building"].heat_transactions
		numpy.save(os.path.join(path_to_save_folder, "heat_transactions"), heat_transactions)

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

	def compute_electricity_bills(self, time, load, demand, supply):

		internal_trade = self.dt*self.prices["internal"][time]*min(demand, supply)

		purchase = internal_trade + self.prices["external_purchase"][time]*max(0, load)*self.dt
		sale = internal_trade + self.prices["external_purchase"][time]*max(0, -load)*self.dt

		for name, player in self.players.items():

			load = player.load[time]

			if load >= 0:
				player.bill[time] += purchase * load / demand
			else:
				player.bill[time] -= sale * load / supply

	def compute_heat_bills(self, time):

		eq = self.players["data_center"].heat_transactions[time]
		heat = eq[0]
		price = eq[1]

		self.players["data_center"].bill -= heat*price
		self.players["smart_building"].bill += heat*price


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('-d', '--data', type=str, required=True, help='folder hosting data')
	parser.add_argument('-s', '--save', type=str, required=True, help='folder to save results')
	parser.add_argument('--simulations', type=int, default=100, help='number of simulations')

	opt = parser.parse_args()

	community = Community(opt.data)
	community.simulate(opt.save, opt.simulations)