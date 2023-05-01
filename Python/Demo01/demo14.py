import numpy as np
import matplotlib.pyplot as plt

# Define PID parameters
Kp = 1.0
Ki = 0.01
Kd = 0.1

# Define initial values
setpoint = 0.0
x = np.random.uniform(0, 2 * np.pi) # Random initial phase difference
integral = 0.0
derivative = 0.0
dt = 0.01 # Time step size
t_end = 10.0 # End time

# Define phase difference function
def phase_diff(t):
    return np.sin(2 * np.pi * 1.0 * t) - np.sin(2 * np.pi * 0.9 * t)

# Define PID function
def pid(x, setpoint, integral, derivative):
    error = setpoint - x
    integral = integral + error * dt
    derivative = (error - pid.last_error) / dt
    pid.last_error = error
    pid_output = Kp * error + Ki * integral + Kd * derivative
    return pid_output, integral, derivative
pid.last_error = 0.0

# Define lock_phase function
def lock_phase():
    global x, integral, derivative
    x_vals = []
    pid_vals = []
    t_vals = np.arange(0, t_end, dt)
    for t in t_vals:
        phase = phase_diff(t)
        pid_output, integral, derivative = pid(x, setpoint, integral, derivative)
        x = x + pid_output * dt
        x = x % (2 * np.pi) # keep x in the range [0, 2*pi]
        x_vals.append(x)
        pid_vals.append(pid_output)
    return x_vals, pid_vals, t_vals

# Lock two lasers in phase
x=1.0
x_vals, pid_vals, t_vals = lock_phase()

# Plot results
plt.plot(t_vals, x_vals)
plt.plot(t_vals, pid_vals)
plt.xlabel('Time (s)')
plt.ylabel('Phase difference')
plt.legend(['Phase difference', 'PID output'])
plt.savefig('b.pdf')
