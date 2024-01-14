import numpy as np
import chatbot_agent_simulation as ca_sim

def run_replication():
    help_center_model = ca_sim.Help_Center()
    # That just returned the whole dataframe for analysis
    #   We are just looking at the mean this time. 
    df_replication = help_center_model.run()
    
    rep_mean = np.nanmean(df_replication['Q_Agent_Time'].tail(int(len(df_replication) * 0.9)))
    print ('{} Agents: {}'.format(ca_sim.g.num_agents, rep_mean))
    return rep_mean

def find_agent_num(desired_wait):
    # Get a baseline mean
    rep_mean = run_replication()

    if rep_mean < desired_wait:
        # If the mean was too low, remove an agent and save money
        while rep_mean < desired_wait:
            ca_sim.g.num_agents -= 1
            rep_mean = run_replication()

    elif rep_mean > desired_wait:
        # If mean was too high, hire agent to lower wait time
        while rep_mean > desired_wait:
            ca_sim.g.num_agents += 1
            rep_mean = run_replication()

    return ca_sim.g.num_agents

def print_output(desired_wait, num_agents):
    print('With an arrival rate of {}, a wait time of {} can be achieved with ~{} agents.'.format(ca_sim.g.arrival_rate, desired_wait, num_agents))
