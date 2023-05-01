import numpy as np
import matplotlib.pyplot as plt

# Define laser frequencies and powers
f1 = 193.1e12  # Frequency of laser 1
f2 = 193.2e12  # Frequency of laser 2
P1 = 1         # Power of laser 1
P2 = 1       # Power of laser 2

# Calculate beat frequency and phase difference
beat_freq = np.abs(f1 - f2)
phase_diff = np.random.uniform(0, 2*np.pi)

# Generate time axis
t = np.linspace(0, 1e-6, 1000)

# Generate two laser signals with random phase
signal1 = P1 * np.sin(2*np.pi*f1*t + np.random.uniform(0, 2*np.pi))
signal2 = P2 * np.sin(2*np.pi*f2*t + phase_diff + np.random.uniform(0, 2*np.pi))

# Combine the two signals
combined_signal = signal1 + signal2

# Plot the signals
fig, ax = plt.subplots(3, 1, figsize=(12, 12))
ax[0].plot(t, signal1, label='Laser 1')
ax[0].plot(t, signal2, label='Laser 2')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude')
ax[0].legend()

# Plot the combined signal
ax[1].plot(t, combined_signal)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Amplitude')

# Plot the power spectrum
power_spectrum = np.abs(np.fft.fft(combined_signal))**2
freq = np.fft.fftfreq(combined_signal.size, t[1]-t[0])
ax[2].plot(freq, power_spectrum)
ax[2].set_xlabel('Frequency (Hz)')
ax[2].set_ylabel('Power')

# Print the beat frequency and phase difference
print(f'Beat frequency: {beat_freq} Hz')
print(f'Phase difference: {phase_diff} rad')

plt.savefig('1.pdf')
