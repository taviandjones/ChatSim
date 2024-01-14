import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import matplotlib.pyplot as plt
import pandas as pd

import a_csv_manager as a_csv_manager
import a_main_helper as mh
import a_chatbot_agent_simulation as ca_sim

a_csv_manager.empty_trial_results_csv()

for i in range(110, 115):
    ca_sim.g.num_agents = i
    wait = mh.run_replication()
    mh.print_output(ca_sim.g.num_agents, wait)

# Make a scatter plot of the data in trail_results.csv

plt.clf()

trial_results = pd.read_csv('trial_results.csv')

plt.scatter(trial_results['Num_Agents'], trial_results['Mean_Q'], s=10)

plt.show()
