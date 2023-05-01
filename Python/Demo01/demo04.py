import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Define the parameters of the lasers
num_lasers = 4
frequency = 200  # MHz
wavelength = 1064  # nm
tau = 0.1  # ns

# Generate random initial phases for each laser
phases = np.random.rand(num_lasers) * 2 * np.pi

# Define the target phase difference between each laser
target_phase_diff = np.pi/2  # radians

# Define the step size for updating the phase
step_size = 0.001  # radians

# Define the time interval for simulation
num_steps = 1000
time_interval = 1/frequency  # microseconds
time_vals = np.arange(num_steps) * time_interval

# Create arrays to store the phase, phase difference, and phase change
phase_vals = np.zeros((num_lasers, num_steps))
phase_diff_vals = np.zeros((num_lasers, num_lasers, num_steps))
phase_change_vals = np.zeros((num_lasers, num_lasers, num_steps))

# Loop through the time steps and update the phases
for i in range(num_steps):
    # Calculate the phase difference between each pair of lasers
    for j in range(num_lasers):
        for k in range(num_lasers):
            phase_diff_vals[j,k,i] = phases[k] - phases[j]

    # Update the phases to minimize the phase difference
    for j in range(num_lasers):
        phase_change = 0
        for k in range(num_lasers):
            if j != k:
                phase_change += np.sin(phase_diff_vals[k,j,i] - target_phase_diff)
        phase_change *= step_size
        phases[j] += phase_change
        phase_change_vals[:,j,i] = phase_change

    phase_vals[:,i] = phases

# Plot the results
fig, axs = plt.subplots(num_lasers+2, 1, figsize=(8, 16))
fig.suptitle('Phase Locking of Ultrafast Fiber Lasers')

# Plot the current phase of each laser
for i in range(num_lasers):
    axs[i].plot(time_vals, phase_vals[i,:])
    axs[i].set_ylabel('Phase (rad)')
    axs[i].set_title('Laser ' + str(i+1))

# Plot the phase difference between each pair of lasers
for i in range(num_lasers):
    for j in range(num_lasers):
        if i != j:
            axs[num_lasers].plot(time_vals, phase_diff_vals[i,j,:])
            axs[num_lasers].set_ylabel('Phase Difference (rad)')
            axs[num_lasers].set_title('Phase Differences')

# Plot the phase changes for each laser
for i in range(num_lasers):
    axs[num_lasers+1].plot(time_vals, phase_change_vals[i,:])
    axs[num_lasers+1].set_xlabel('Time (us)')
    axs[num_lasers+1].set_ylabel('Phase Change (rad)')
    axs[num_lasers+1].set_title('Phase Changes')

# Save the figure to a file with a timestamp
now = datetime.now()
timestamp = now.strftime('%Y%m%d_%H%M%S')
fig.savefig('laser_phases_' + timestamp + '.png')

# Show the figure
plt.show()
