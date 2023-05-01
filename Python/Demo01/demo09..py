import numpy as np
import matplotlib.pyplot as plt

# Define laser parameters
wavelength = 1550e-9 # meters
P = 10 # watts

# Define cavity parameters
L = 1 # meters
finesse = 200
mode_spacing = 3e8 / (2 * L * finesse)

# Define feedback loop parameters
gain = 1
proportional_gain = 0.1
integral_gain = 0.01

# Define simulation parameters
dt = 1e-8
t = np.arange(0, 1e-5, dt)
noise_amplitude = 0.01

# Initialize laser phases
phase1 = np.random.rand() * 2 * np.pi
phase2 = np.random.rand() * 2 * np.pi

# Initialize feedback loop variables
frequency_error_integral = 0
phase_error_integral = 0

# Initialize phase difference array
phase_diff = np.zeros_like(t)

# Loop over time steps
for i in range(len(t)):
    # Calculate laser frequencies
    frequency1 = 3e8 / wavelength - P / (2 * np.pi * L) * np.sin(phase1)
    frequency2 = 3e8 / wavelength - P / (2 * np.pi * L) * np.sin(phase2)
    
    # Add noise to frequencies
    frequency1 += noise_amplitude * np.random.randn()
    frequency2 += noise_amplitude * np.random.randn()
    
    # Calculate cavity resonance frequencies
    cavity_freq1 = np.round(frequency1 / mode_spacing) * mode_spacing
    cavity_freq2 = np.round(frequency2 / mode_spacing) * mode_spacing
    
    # Calculate frequency error signals
    frequency_error1 = cavity_freq1 - frequency1
    frequency_error2 = cavity_freq2 - frequency2
    
    # Integrate frequency error signals
    frequency_error_integral += frequency_error1 * dt
    frequency_error_integral += frequency_error2 * dt
    
    # Calculate phase error signal
    phase_error = phase2 - phase1
    
    # Integrate phase error signal
    phase_error_integral += phase_error * dt
    
    # Calculate feedback signals
    frequency_feedback = -proportional_gain * frequency_error_integral
    phase_feedback = -integral_gain * phase_error_integral
    
    # Apply feedback to laser phases
    phase1 += 2 * np.pi * gain * (frequency_feedback + phase_feedback) * dt
    phase2 += 2 * np.pi * gain * (-frequency_feedback + phase_feedback) * dt
    
    # Calculate phase difference
    phase_diff[i] = phase2 - phase1

# Plot phase difference
plt.plot(t, phase_diff)
plt.xlabel('Time (s)')
plt.ylabel('Phase difference (rad)')
plt.savefig('phase01.pdf')
