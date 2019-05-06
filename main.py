import numpy as np
import os

from players.charging_station import ChargingStation
from players.data_center import DataCenter
from players.smart_building import SmartBuilding
from players.solar_farm import SolarFarm

import np.random.randint as randint


class Community:

	def __init__(path_to_data_folder):

		self.horizon = 48
		self.path_to_data_folder = path_to_data_folder

		self.charging_station = ChargingStation()
		self.data_center = DataCenter()
		self.smart_building = SmartBuilding()
		self.solar_farm = SolarFarm()

	def play():

		for t in range(self.horizon):

			self.call_loads()

		return 0

	def call_loads():

		return 0




