import numpy as np
import matplotlib.pyplot as plt

# 设置常数
dt = 0.01    # 时间步长
T = 1000     # 总时间
w1 = 0.1     # 激光1频率
w2 = 0.09    # 激光2频率
phi1 = 0    # 激光1的初始相位
phi2 = 0.5*np.pi    # 激光2的初始相位
Kp = 1       # 比例系数
Ki = 0.1     # 积分系数
Kd = 0.1     # 微分系数
error_sum = 0  # 记录误差累计值
last_error = 0 # 记录上一个误差值

# 定义相位差函数
def phase_diff(phi1, phi2):
    return phi1 - phi2

# 计算初始相位差
phi_diff = phase_diff(phi1, phi2)

# 初始化数组
time = np.arange(0, T, dt)

# 迭代计算相位差随时间的变化
for i in range(1, len(time)):
    phi1 += w1 * dt
    phi2 += w2 * dt
    error = phase_diff(phi1, phi2) - phi_diff

    # 计算PID控制量
    error_sum += error * dt
    error_diff = (error - last_error) / dt
    control = Kp * error + Ki * error_sum + Kd * error_diff
    last_error = error

    # 更新激光1的相位
    phi1 -= control

    # 更新相位差
    phi_diff = phase_diff(phi1, phi2)

    # 如果相位差接近零，停止迭代
    if np.abs(phi_diff) < 1e-3:
        break

# 绘制相位差随时间的变化图
plt.plot(time[:i], phi_diff * np.ones_like(time[:i]))
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Phase Difference')
plt.title('Phase Locking of Two Lasers with PID Control')
plt.savefig('17-0.pdf')
