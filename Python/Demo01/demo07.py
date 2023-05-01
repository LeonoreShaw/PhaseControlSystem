import numpy as np
import matplotlib.pyplot as plt
import time

# Define laser parameters
freqs = [10e6, 15e6, 20e6]  # Laser frequencies in Hz
phases = [0.2, 0.3, 0.4]    # Initial laser phases
error_integrals = [0.0, 0.0, 0.0]  # Error integrals for PID control
error_thresholds = [0.1, 0.1, 0.1]  # Error thresholds for PID control

# Define PID parameters
Kp = 0.1
Ki = 0.01
Kd = 0.001

# Define time parameters
t_start = 0
t_end = 0.1
dt = 1e-8
t = np.arange(t_start, t_end, dt)

# Define arrays for phase and error over time
phase_history = np.zeros((len(t), len(freqs)))
error_history = np.zeros((len(t), len(freqs)))

# Define function to calculate phase error
def calc_phase_error(phases, freqs):
    # Calculate phase differences between lasers
    phase_diffs = np.diff(phases)
    # Calculate frequency differences between lasers
    freq_diffs = np.diff(freqs)
    # Calculate phase errors
    phase_errors = (phase_diffs - freq_diffs * (t[1]-t[0])) % (2*np.pi)
    return phase_errors

# Main loop
for i in range(len(t)):
    # Calculate current phase errors
    phase_errors = calc_phase_error(phases, freqs)
    # Update error integrals
    error_integrals += phase_errors*dt
    # Calculate error derivatives
    if i == 0:
        error_derivatives = np.zeros(len(freqs))
    else:
        error_derivatives = (phase_errors - error_history[i-1]) / dt
    # Calculate PID control signals
    control_signals = Kp*phase_errors + Ki*error_integrals + Kd*error_derivatives
    # Update laser phases
    phases -= control_signals
    # Record phase and error histories
    phase_history[i,:] = phases
    error_history[i,:] = phase_errors
    # Check if error is below threshold
    if np.all(np.abs(phase_errors) < error_thresholds):
        print('Lock achieved at t = {:.2e}'.format(t[i]))
        break

# Plot phase errors over time
fig, axs = plt.subplots(nrows=3, sharex=True, figsize=(10,6))
for i in range(len(freqs)):
    axs[i].plot(t, error_history[:,i], label='Laser {}'.format(i+1))
    axs[i].set_ylabel('Phase Error (rad)')
    axs[i].legend()
axs[-1].set_xlabel('Time (s)')

# Save plot to file
plt.savefig('phase_errors.png')
plt.show()
