import matplotlib.pyplot as plt
import pandas as pd

# Load the data
plt.clf()

data = pd.read_csv('50000-6.csv')

plt.scatter(data['Num_Agents'], data['Mean_Q'], s=10)

plt.show()