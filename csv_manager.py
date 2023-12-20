import pandas as pd

# These two functions empty their respective csvs.
# These are optional and can be used if needed.
# Note, the functions to write to csvs are in chatbot_agent_simulation.py. 
def empty_trial_results_csv():
    with open('trial_results.csv', 'w') as file:
        trial_results_columns = pd.DataFrame(columns=['Mean_Q'])
        trial_results_columns.to_csv('trial_results.csv', index=False)


def empty_raw_data_csv():
    with open('raw_data.csv', 'w') as file:
        raw_data_columns = pd.DataFrame(columns=['C_ID', 'Q_Agent_Time', 'First_Path', 'Did_Queue', 'Queue_Length'])
        raw_data_columns.to_csv('raw_data.csv', index=False)