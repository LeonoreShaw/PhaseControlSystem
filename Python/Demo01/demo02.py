import numpy as np
import time
import matplotlib.pyplot as plt

# Define laser parameters
laser_freq = np.array([10.0, 11.0])  # Frequency of each laser in GHz
laser_phase = np.array([0.0, 0.0])  # Initial phase of each laser in radians
laser_amplitude = np.array([1.0, 1.0])  # Amplitude of each laser

# Define feedback parameters
feedback_gain = 0.1  # Feedback gain
target_phase_diff = np.pi / 2  # Target phase difference in radians

# Initialize feedback loop
phase_diff = np.zeros(1000)  # Array to store phase difference over time
time_vals = np.arange(0, 1000)  # Array of time values
start_time = time.time()  # Record start time

# Run feedback loop
for i in range(1000):
    # Measure interference pattern
    interference_pattern = laser_amplitude[0] * np.sin(2 * np.pi * laser_freq[0] * i / 1000 + laser_phase[0]) \
                         + laser_amplitude[1] * np.sin(2 * np.pi * laser_freq[1] * i / 1000 + laser_phase[1])

    # Calculate phase difference
    phase_diff[i] = np.arctan2(laser_amplitude[1] * np.sin(2 * np.pi * laser_freq[1] * i / 1000 + laser_phase[1]),
                               laser_amplitude[0] * np.sin(2 * np.pi * laser_freq[0] * i / 1000 + laser_phase[0]))

    # Adjust phase of lasers
    laser_phase += feedback_gain * (target_phase_diff - phase_diff[i])

# Print final results
print("Phase difference after 1000 iterations:", phase_diff[-1])
print("Time elapsed:", time.time() - start_time, "seconds")

# Plot phase difference vs time
plt.plot(time_vals, phase_diff)
plt.xlabel("Time (ms)")
plt.ylabel("Phase difference (rad)")
plt.title("Real-time phase locking of two lasers")
plt.show()
