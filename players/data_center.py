import numpy as np
import os
from numpy.random import randint
import matplotlib.pyplot as plt

class DataCenter:

    def __init__(self, path_to_data_folder):

        self.path_to_data_folder = path_to_data_folder
        self.bill = np.zeros(48)
        self.n_data = 10
        self.scenario = {}


    def load(self,time):

        return 0

    def draw_random_scenario(self):

        test_load_data_center = np.loadtxt(os.path.join(self.path_to_data_folder, "data-center",
                                                        "test_load_data-center.csv"))
        self.scenario["load_data_center"] = test_load_data_center[randint(self.n_data), :]

    def plot_scenario(self):
        plt.plot(range(0,len(self.scenario["load_data_center"])),self.scenario["load_data_center"])
