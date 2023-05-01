import numpy as np
import matplotlib.pyplot as plt

# 设置常数
dt = 0.01    # 时间步长
T = 1000     # 总时间
w1 = 0.1     # 激光1频率
w2 = 0.09    # 激光2频率
phi1 = 0    # 激光1的初始相位
phi2 = 0.32*np.pi    # 激光2的初始相位

# 定义相位差函数
def phase_diff(phi1, phi2):
    return np.sin(phi1) - np.sin(phi2)

# 初始化数组
time = np.arange(0, T, dt)
phi_diff = np.zeros_like(time)

# 迭代计算相位差随时间的变化
for i in range(1, len(time)):
    phi1 += w1 * dt
    phi2 += w2 * dt
    phi_diff[i] = phase_diff(phi1, phi2)

    # 如果相位差接近零，停止迭代
    if np.abs(phi_diff[i]) < 1e-3:
        break

# 绘制相位差随时间的变化图
plt.plot(time[:i], phi_diff[:i])
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Phase Difference')
plt.title('Phase Locking of Two Lasers')
plt.savefig('yes.pdf')
