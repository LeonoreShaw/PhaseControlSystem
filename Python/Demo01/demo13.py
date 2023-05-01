import numpy as np
import matplotlib.pyplot as plt

# Parameters
dt = 0.01
setpoint = 0.0
Kp = 0.01
Ki = 0.01
Kd = 0.01
integral = 0.0
derivative = 0.0

# Generate random phase difference
phase_diff = np.random.uniform(low=-np.pi, high=np.pi, size=1000)

def pid(x, setpoint, integral, derivative):
    error = setpoint - x
    integral = integral + error * dt
    derivative = (error - pid.last_error) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    pid.last_error = error
    return output, integral, derivative
pid.last_error = 0.0

def lock_phase():
    global x, integral, derivative
    x_vals = []
    pid_vals = []
    for i in range(len(phase_diff)):
        pid_output, integral, derivative = pid(x, setpoint, integral, derivative)
        x = x + pid_output * dt
        x = x % (2 * np.pi) # keep x in the range [0, 2*pi]
        x_vals.append(x)
        pid_vals.append(pid_output)
    return x_vals, pid_vals
x=1.0
x_vals, pid_vals = lock_phase()

plt.plot(x_vals)
plt.plot(pid_vals)
plt.xlabel('Time step')
plt.ylabel('Phase difference')
plt.legend(['Phase difference', 'PID output'])
plt.savefig('a.pdf')
