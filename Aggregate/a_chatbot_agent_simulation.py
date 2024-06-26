import simpy
import pandas as pd
import numpy as np
import csv
import random
import math
import matplotlib.pyplot as plt
import time


class g:
    desired_customers = 10000

    arrival_rate = 6
    num_agents = 100

    t_agent = 20
    t_bot = 20
    p_success = 0.5

    c_line = 0.221
    c_agent = 0.240
    c_bot = 0.288
    beta = 1.170


class Customer:
    # Each customer has these four attributes
    # Each attribute will be set as it travels through
    # the simulation and used for the collection of data
    def __init__(self, c_id):
        self.id = c_id
        self.q_agent_time = np.nan
        self.first_path = 'Unknown'
        self.did_queue = False
        self.queue_length = np.nan


class Display:
    # Initializes the display
    fig, ax = plt.subplots(nrows = 2, ncols = 2)


class Help_Center:
    def __init__(self):
        # Initializes the simulation environment and sets resource
        self.env = simpy.Environment()
        self.agent = simpy.Resource(self.env, capacity = g.num_agents)
    
        self.customer_counter = 0
        self.df_individual_run = pd.DataFrame(columns=['C_ID', 'Q_Agent_Time', 'First_Path', 'Did_Queue', 'Queue_Length'])
        self.df_time_arrays = pd.DataFrame(columns=['Time_Array'])

    def generate_customer_arrivals(self):
        while self.customer_counter < g.desired_customers:
            cus = Customer(self.customer_counter) 
            try:
                # This returns the probability of agent in a few steps
                # First, it looks through the dataframe of the time arrays.
                #   Remember that each array is a list of times, and the index
                #   of that array is how many people were in front of that 
                #   person in line. Hence the iloc[].
                # Second, it takes the average of that array. 
                #   This is the average wait time of people who had the same 
                #   number of people  in front
                # Third, it runs the return_prob_agent function on that number
                #   to turn that displayed wait time into the probability
                historical_wait_time = np.array(self.df_time_arrays.iloc[len(self.agent.queue), 0]).mean()
                prob_agent = self.return_prob_agent(historical_wait_time)
            except:
                estimated_wait_time = (len(self.agent.queue) * g.t_agent) / g.num_agents + (g.t_agent / 2)
                prob_agent = self.return_prob_agent(estimated_wait_time)
            
            if random.random() <= prob_agent: 
                cus.first_path = 'Agent'
                self.env.process(self.enter_agent_center(cus))
            else:
                cus.first_path = 'Bot'
                self.env.process(self.enter_chatbot_center(cus))
            self.customer_counter += 1
            yield self.env.timeout(random.expovariate(g.arrival_rate))

    def enter_chatbot_center(self, customer):
        # Wait time for chatbot is always the same
        yield self.env.timeout(g.t_bot)
        # If successful, update its data and add it to the dataframe
        if random.random() <= g.p_success:
            df_to_add = pd.DataFrame({'C_ID':[customer.id],
                                    'Q_Agent_Time': [customer.q_agent_time],
                                    'First_Path': [customer.first_path],
                                    'Did_Queue': [customer.did_queue],
                                    'Queue_Length': [customer.queue_length]})
            self.df_individual_run = pd.concat([self.df_individual_run, df_to_add], ignore_index=True)
        # If unsuccessful, send it to the agent center
        else:
            self.env.process(self.enter_agent_center(customer))


    def enter_agent_center(self, customer):
        # Update the customers data
        customer.did_queue = True
        customer.queue_length = len(self.agent.queue)
        
        q_agent_start = self.env.now
        with self.agent.request() as req:
            yield req
            # Add the customer to the main df
            customer.q_agent_time = self.env.now - q_agent_start
            df_to_add = pd.DataFrame({'C_ID':[customer.id],
                                      'Q_Agent_Time': [customer.q_agent_time],
                                      'First_Path': [customer.first_path],
                                      'Did_Queue': [customer.did_queue],
                                      'Queue_Length': [customer.queue_length]})
            self.df_individual_run = pd.concat([self.df_individual_run, df_to_add], ignore_index=True)
            
            while True:
                # Put its empirical wait time into the dataframe of time arrays
                    #   for later use in estimation
                try:
                    # Almost always happens, this is the normal case
                    self.df_time_arrays.iloc[customer.queue_length, 0].append(customer.q_agent_time)
                    break
                except:
                    # Creates a new row, this happens when a customer is 
                    #   the first to reach a new queue length in front of them
                    time_array_to_add = pd.DataFrame({'Time_Array': [[]]})
                    self.df_time_arrays = pd.concat([self.df_time_arrays, time_array_to_add], ignore_index=True)
            
            yield self.env.timeout(g.t_agent)

    def write_trial_results(self):
        mean_q_agent_time = np.nanmean(self.df_individual_run['Q_Agent_Time'].tail(int(len(self.df_individual_run) * 0.9)))
        existing_data = pd.read_csv('trial_results.csv')
        df_to_add = pd.DataFrame({'Num_Agents': [g.num_agents],
                                  'Mean_Q': [mean_q_agent_time]})
        existing_data = pd.concat([existing_data, df_to_add], ignore_index=True)
        existing_data.to_csv('trial_results.csv', index=False)

    def return_prob_agent(self, live_displayed_wait):
        # Uses the displayed wait time in the probability calculation to return a number from 0-1
        utility_a = -g.c_line * live_displayed_wait - g.c_agent * g.t_agent
        utility_b = -g.c_bot * g.t_bot - (1-g.p_success) * g.beta * (g.c_line * live_displayed_wait + g.c_agent * g.t_agent)
        return math.e ** utility_a / (math.e ** utility_a + math.e ** utility_b)

    def run(self):
        self.env.process(self.generate_customer_arrivals())
        self.env.run()
        self.write_trial_results()

        return self.df_individual_run