import numpy 
import os

from players.charging_station import ChargingStation
from players.data_center import DataCenter
from players.smart_building import SmartBuilding
from players.solar_farm import SolarFarm


class Community:

	def __init__(self, path_to_data_folder):

		self.horizon = 48
		self.path_to_data_folder = path_to_data_folder

		self.charging_station = ChargingStation(path_to_data_folder)
		self.data_center = DataCenter(path_to_data_folder)
		self.smart_building = SmartBuilding(path_to_data_folder)
		self.solar_farm = SolarFarm(path_to_data_folder)

		self.loads = {"charging_station", "data_center", "smart_building", "solar_farm"}

	def play(self):

		for t in range(self.horizon):

			self.call_loads(t)

		return 0

	def call_loads(self, time):

		self.loads["charging_station"] = self.charging_station.load(time)
		self.loads["data_center"] = self.data_center.load(time)
		self.loads["smart_building"] = self.smart_building.load(time)
		self.loads["solar_farm"] = self.solar_farm.load(time)

		return 0




