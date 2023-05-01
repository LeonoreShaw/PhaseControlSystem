import numpy as np
import matplotlib.pyplot as plt

# Define laser parameters
N = 4
laser_freqs = np.array([0.5, 0.6, 0.7, 0.8])  # in GHz
laser_phases = np.random.rand(N) * 2 * np.pi
laser_output = np.zeros(N)

# Define feedback parameters
Kp = 0.1
Ki = 0.01
Kd = 0.001
setpoint = 0

# Define PID variables
last_error = 0
integral = 0

# Define plotting variables
time_steps = 5000
time_axis = np.arange(time_steps)
phases_axis = np.zeros((time_steps, N))
output_axis = np.zeros((time_steps, N))
new_phases_axis = np.zeros((time_steps, N))
current_phases_axis = np.zeros((time_steps, N))

# Start phase locking loop
for i in range(time_steps):
    # Calculate current phase error and update PID variables
    error = setpoint - np.sum(laser_output * laser_freqs)
    integral += error
    derivative = error - last_error
    last_error = error

    # Calculate new laser phases and update laser output
    new_phases = laser_phases + Kp * error + Ki * integral + Kd * derivative
    laser_output = np.sin(new_phases)

    # Update plotting variables
    phases_axis[i] = laser_phases
    output_axis[i] = laser_output
    new_phases_axis[i] = new_phases
    current_phases_axis[i] = laser_phases + 2*np.pi*laser_freqs*i/1000

    # Update laser phases
    laser_phases = new_phases

# Plot results
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))
ax[0, 0].plot(time_axis, current_phases_axis)
ax[0, 0].set_title('Current Laser Phases')
ax[0, 0].set_xlabel('Time')
ax[0, 0].set_ylabel('Phase (rad)')

ax[0, 1].plot(time_axis, output_axis)
ax[0, 1].set_title('Laser Output')
ax[0, 1].set_xlabel('Time')
ax[0, 1].set_ylabel('Amplitude')

ax[1, 0].plot(time_axis, phases_axis)
ax[1, 0].set_title('Laser Phases')
ax[1, 0].set_xlabel('Time')
ax[1, 0].set_ylabel('Phase (rad)')

ax[1, 1].plot(time_axis, new_phases_axis)
ax[1, 1].set_title('New Laser Phases')
ax[1, 1].set_xlabel('Time')
ax[1, 1].set_ylabel('Phase (rad)')

# Save plot
plt.savefig('phase_locking_plot02.pdf')
# plt.savefig('phase_locking_plot02.png', dpi=1000)
