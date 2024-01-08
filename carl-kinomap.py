
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the kinomap data
race = pd.read_csv("carl.csv")

# drop location columns, I'm not really moving on the ergometer
race.drop(['Latitude', 'Longitude', 'Altitude'], axis=1, inplace=True)
# drop rows with no data for heart rate
# race = race[race['Heart rate'] > 80]
# race = race[race['Power'] > 50]

# extract heart rate column as array so as to smooth it
heart_rat_array = np.array(race['Heart rate'])
smooth_heart_rat_array = np.zeros(len(heart_rat_array))
for t in range(15, len(smooth_heart_rat_array)-15):
    for i in range(-15, 15):
        smooth_heart_rat_array[t] += heart_rat_array[t+i]
    smooth_heart_rat_array[t] /= 30

# add smooted heart rate column to dataframe
race["Smooth heart rate"] = smooth_heart_rat_array
race = race[race['Smooth heart rate'] > 100]


# Convert Date column to time in seconds
race['Seconds'] = pd.to_datetime(race['Date']).astype(np.int64) // 10**9

# Calculate the duration in minutes since the start of the session
race['Duration'] = (race['Seconds'] - race['Seconds'].iloc[0])/60
race = race[(race['Duration'] < 12.0) | (race['Duration'] > 15.8)]


# Fit linearly the Power to the Heart rate
fit = np.polyfit(race['Power'][120:12*60],
                 race['Smooth heart rate'][120:12*60], 1)

# Get the slope and intercept of the linear fit
slope = fit[0]
intercept = fit[1]
print(slope, intercept)
print("Slope:", slope)
print("Intercept:", intercept)
print(f"PWC170:: {(170-intercept)/slope:.2f} (W)")

# Plot Heart rate and power vs Duration with independent y axis
fig1, (ax1, ax3) = plt.subplots(1, 2, figsize=(12, 7))
ax1.plot(race['Duration'], race['Smooth heart rate'],
         color='red', linewidth=3, label='Heart rate')
ax1.set_ylim(bottom=125)

ax1.set_xlabel('Duration(min)')
ax1.set_ylabel('Heart rate(bpm )', color='red')
ax1.set_title('Heart rate and Power vs Duration')
heart_interval = np.arange(125, 200, 5)
ax1.set_yticks(list(range(125, 200, 5)))
ax1.legend(shadow=True, fontsize='x-large', loc='upper left')


ax2 = ax1.twinx()

# Plot Power vs Duration
ax2.plot(race['Duration'], race['Power'], color='blue', label='Power')
ax2.set_ylabel('Power(W)', color='blue')

ax2.legend(shadow=True, fontsize='x-large', loc='lower left')
# Show grid

ax1.grid(True)


# Plot Heart rate vs Duration
ax3.plot(race.Power, race["Smooth heart rate"], color='green',
         marker='o',  linewidth=3, markersize=5)
ax3.set_xlabel('Power(W)', color='blue')
ax3.set_ylabel('Heart rate(bpm)', color='red')
ax3.set_title('Heart rate vs Power')


# Print the slope and intercept

# # Calculate the fitted values
fit_values = slope * race['Power'] + intercept

# # Plot the fit
ax3.plot(race['Power'], fit_values, color='orange', linewidth=2, label='Fit')

# Add legend to ax3
ax3.legend(shadow=True, fontsize='x-large', loc='upper left')


plt.tight_layout()

# Add Git parameters to the plot


# Display fit parameters on the second plot
ax3.text(0.80, 0.05, f'Pulse = {slope:.2f}*Power + {intercept:.2f}\n' +
         f'Power = {(1/slope):.2f}*(Pulse-{intercept:.2f})\n' +
         f'PWCMAX:: {(196-intercept)/slope:.2f} (W)\n' +
         f'PWC170:: {(170-intercept)/slope:.2f} (W)\n' +
         f"PWC150:: {(150-intercept)/slope:.2f} (W)\n",
         transform=ax3.transAxes, ha='right', va='bottom')

plt.savefig('carl.pdf')
plt.savefig('carl.png')

plt.show()
