import numpy as np

class DataCenter:

	def __init__(path_to_data_folder):

		self.path_to_data_folder = path_to_data_folder
		self.bill = np.zeros(48)
		self.n_data = 10


	def load(time):

		return 0

	def draw_random_scenario():

		test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "data-center",
			"test_load_data-center.csv"))
		self.scenario["load_data_center"] = test_load_data_center[randint(self.n_data), :]

