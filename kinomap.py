
import pandas as pd
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt

race = pd.read_csv("race.csv")

race.drop(['Latitude', 'Longitude', 'Altitude'], axis=1, inplace=True)
race = race[race['Heart rate'] > 50]

heart_rat_array = np.array(race['Heart rate'])
print(len(heart_rat_array))
smooth_heart_rat_array = np.zeros(len(heart_rat_array))
for t in range(15, len(smooth_heart_rat_array)-15):
    for i in range(-15, 15):
        smooth_heart_rat_array[t] += heart_rat_array[t+i]
    smooth_heart_rat_array[t] /= 30

race["Smooth heart rate"] = smooth_heart_rat_array
race = race[race['Smooth heart rate'] > 75]

# Convert Date column to time in seconds
race['Seconds'] = pd.to_datetime(race['Date']).astype(np.int64) // 10**9

# Calculate the duration in seconds of the first row
race['Duration'] = (race['Seconds'] - race['Seconds'].iloc[0])/60

# Plot Heart rate vs Duration
fig1, (ax1, ax3) = plt.subplots(1, 2, figsize=(12, 7))
ax1.plot(race['Duration'], race['Smooth heart rate'],
         color='red', linewidth=3, label='Heart rate')
ax1.set_xlabel('Duration')
ax1.set_ylabel('Heart rate')
ax1.set_title('Heart rate and  vs Duration')
heart_interval = np.arange(70, 135, 5)
ax1.set_yticks(list(range(75, 130, 5)))
ax1.legend(shadow=True, fontsize='x-large', loc='upper left')


ax2 = ax1.twinx()

# Plot Power vs Duration
ax2.plot(race['Duration'], race['Power'], color='blue', label='Power')
ax2.set_ylabel('Power', color='blue')
ax2.set_title('Heart rate and  vs Duration')
ax2.legend(shadow=True, fontsize='x-large', loc='lower left')
# Show grid

ax1.grid(True)

# Set minor y ticks on ax1

# Plot Heart rate vs Duration
ax3.plot(race.Power, race["Smooth heart rate"], color='green',
         marker='o',  linewidth=3, markersize=5)
ax3.set_xlabel('Power', color='blue')
ax3.set_ylabel('Heart rate', color='red')
ax3.set_title('Heart rate vs Power')

plt.show()
