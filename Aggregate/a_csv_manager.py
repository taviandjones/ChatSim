import pandas as pd

# Note, the functions to write to csvs are in chatbot_agent_simulation.py. 
def empty_trial_results_csv():
    with open('trial_results.csv', 'w') as file:
        trial_results_columns = pd.DataFrame(columns=['Num_Agents', 'Mean_Q'])
        trial_results_columns.to_csv('trial_results.csv', index=False)