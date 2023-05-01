import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
dt = 0.01          # time step
T = 100            # total simulation time
K = 0.1            # feedback gain
f0 = 1             # laser frequency
phi0_1 = 0         # initial phase of laser 1
phi0_2 = np.pi/2   # initial phase of laser 2

# Initialize the arrays
t = np.arange(0, T, dt)          # time array
phi_1 = np.zeros_like(t) + phi0_1   # phase array for laser 1
phi_2 = np.zeros_like(t) + phi0_2   # phase array for laser 2
y = np.zeros_like(t)            # output array

# Define the feedback loop
for i in range(1, len(t)):
    # Compute the current phase difference
    dphi = phi_2[i-1] - phi_1[i-1]
    
    # Compute the output
    y[i] = np.sin(phi_1[i-1]) + np.sin(phi_2[i-1])
    
    # Update the phase of laser 1
    dphi_1 = 2*np.pi*f0*dt + K*y[i]*np.sin(dphi)
    phi_1[i] = phi_1[i-1] + dphi_1
    
    # Update the phase of laser 2
    dphi_2 = 2*np.pi*f0*dt + K*y[i]*np.sin(-dphi)
    phi_2[i] = phi_2[i-1] + dphi_2
    
# Plot the results
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))

ax[0].plot(t, phi_1, label='Laser 1')
ax[0].plot(t, phi_2, label='Laser 2')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Phase')
ax[0].legend()

ax[1].plot(t, y)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Output')

# Save the plot
plt.savefig('phase_locking_2lasers.png')

# Show the plot
plt.show()
