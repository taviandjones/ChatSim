import matplotlib.pyplot as plt
import numpy as np
import time

# Create a 2x2 grid of subplots
fig, ax = plt.subplots(nrows=2, ncols=2)

# Some sample data for each subplot
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(2 * x)
y4 = np.cos(2 * x)

# Plot data on each subplot
ax[0, 0].plot(x, y1, label='sin(x)')
ax[0, 0].set_title('Subplot 1')
ax[0, 0].legend()

ax[0, 1].plot(x, y2, label='cos(x)')
ax[0, 1].set_title('Subplot 2')
ax[0, 1].legend()

ax[1, 0].plot(x, y3, label='sin(2x)')
ax[1, 0].set_title('Subplot 3')
ax[1, 0].legend()

# Plot data on Subplot 4 (without calling legend() initially)
line, = ax[1, 1].plot(x, y4, label='cos(2x)')
ax[1, 1].set_title('Subplot 4')

# Adjust spacing between subplots
plt.tight_layout()
plt.pause(2)
# Show the initial plot

# Update data on Subplot 4 and refresh only that subplot
y4_updated = np.sin(3 * x)  # Some updated data
line.set_ydata(y4_updated)  # Update the y-data for Subplot 4
ax[1, 1].relim()  # Recalculate data limits for Subplot 4
ax[1, 1].autoscale_view()  # Autoscale the axes for Subplot 4

# Refresh only Subplot 4
fig.canvas.draw_idle()

# Keep the plot window open
plt.show()