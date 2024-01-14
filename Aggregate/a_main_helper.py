import numpy as np
import a_chatbot_agent_simulation as ca_sim

def run_replication():
    help_center_model = ca_sim.Help_Center()
    
    df_replication = help_center_model.run()
    
    rep_mean = np.nanmean(df_replication['Q_Agent_Time'].tail(int(len(df_replication) * 0.9)))
    
    return rep_mean

def print_output(num_agents, wait):
    print('{}: {}'.format(num_agents, wait))
