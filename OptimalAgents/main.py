import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import matplotlib.pyplot as plt
import csv_manager
import main_helper as mh

print("Hello World")
# Initialize the plot
# This is one of many ways to do this, I have chosen to use 
# a specific functionality of matplotlib, but you do not 
# need to do it this way. 
plt.ion()
plt.show(block=False)

csv_manager.empty_raw_data_csv()
csv_manager.empty_trial_results_csv()

desired_wait = float(input('What is the desired wait time? '))

num_agents = mh.find_agent_num(desired_wait)

mh.print_output(desired_wait, num_agents)