
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


race = pd.read_csv("race.csv")

# drop location columns, I'm not really moving
race.drop(['Latitude', 'Longitude', 'Altitude'], axis=1, inplace=True)

# drop columns with no data for heart rate
race = race[race['Heart rate'] > 50]
# extract heart rate column as array so as to smooth it
heart_rat_array = np.array(race['Heart rate'])
smooth_heart_rat_array = np.zeros(len(heart_rat_array))
for t in range(15, len(smooth_heart_rat_array)-15):
    for i in range(-15, 15):
        smooth_heart_rat_array[t] += heart_rat_array[t+i]
    smooth_heart_rat_array[t] /= 30

# add smooted heart rate column to dataframe
race["Smooth heart rate"] = smooth_heart_rat_array
race = race[race['Smooth heart rate'] > 75]

# Convert Date column to time in seconds
race['Seconds'] = pd.to_datetime(race['Date']).astype(np.int64) // 10**9

# Calculate the duration in minutes since the start of the session
race['Duration'] = (race['Seconds'] - race['Seconds'].iloc[0])/60

# Plot Heart rate and power vs Duration with independent y axis
fig1, (ax1, ax3) = plt.subplots(1, 2, figsize=(12, 7))
ax1.plot(race['Duration'], race['Smooth heart rate'],
         color='red', linewidth=3, label='Heart rate')
ax1.set_xlabel('Duration(min)')
ax1.set_ylabel('Heart rate(bpm )', color='red')
ax1.set_title('Heart rate and Power vs Duration')
heart_interval = np.arange(70, 135, 5)
ax1.set_yticks(list(range(75, 130, 5)))
ax1.legend(shadow=True, fontsize='x-large', loc='upper left')


ax2 = ax1.twinx()

# Plot Power vs Duration
ax2.plot(race['Duration'], race['Power'], color='blue', label='Power')
ax2.set_ylabel('Power(W)', color='blue')

ax2.legend(shadow=True, fontsize='x-large', loc='lower left')
# Show grid

ax1.grid(True)

# Set minor y ticks on ax1

# Plot Heart rate vs Duration
ax3.plot(race.Power, race["Smooth heart rate"], color='green',
         marker='o',  linewidth=3, markersize=5)
ax3.set_xlabel('Power(W)', color='blue')
ax3.set_ylabel('Heart rate(bpm)', color='red')
ax3.set_title('Heart rate vs Power')

plt.tight_layout()

plt.savefig('kinomap.pdf')
plt.savefig('kinomap.png')

plt.show()
