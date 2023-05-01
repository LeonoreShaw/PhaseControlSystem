import numpy as np
import matplotlib.pyplot as plt

# Define PID parameters
Kp = 0.1
Ki = 0.01
Kd = 0.001

# Define the setpoint
setpoint = 0.1

# Define initial values
x = 0.0
integral = 0.0
derivative = 0.0

# Define simulation parameters
dt = 0.001
t = np.arange(0, 10, dt)

# Define the phase difference between the two lasers as a sinusoidal wave
phase_diff = 0.1 * np.sin(2 * np.pi * t)

# Define a function to calculate the PID output
def pid(x, setpoint, integral, derivative):
    error = setpoint - x
    integral = integral + error * dt
    derivative = (error - derivative) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    return output, integral, derivative

# Define a function to simulate the phase locking process
def lock_phase():
    global x, integral, derivative # Add this line to make sure x is recognized as a global variable
    x_vals = []
    pid_vals = []
    for i in range(len(phase_diff)):
        pid_output, integral, derivative = pid(x, setpoint, integral, derivative)
        x = x + pid_output * dt
        x = x % (2 * np.pi) # keep x in the range [0, 2*pi]
        x_vals.append(x)
        pid_vals.append(pid_output)
    return x_vals, pid_vals

# Run the simulation
x_vals, pid_vals = lock_phase()

# Plot the phase difference and the PID output
plt.subplot(2, 1, 1)
plt.plot(t, phase_diff, label='Phase difference')
plt.plot(t, x_vals, label='Locked phase')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, pid_vals, label='PID output')
plt.legend()

plt.savefig('11.pdf')
