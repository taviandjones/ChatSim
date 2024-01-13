import matplotlib.pyplot as plt
import pandas as pd

# Load the data
plt.clf()

data = pd.read_csv('raw_data.csv')


plt.scatter(data['C_ID'].tail(int(len(data) * 0.1)), data['Q_Agent_Time'].tail(int(len(data) * 0.1)), s=1)

plt.show()