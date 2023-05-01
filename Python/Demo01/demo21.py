import numpy as np
import matplotlib.pyplot as plt

# 设置模拟时间和时间步长
t_end = 1  # 模拟结束时间
dt = 0.001  # 时间步长

# 设置PID参数
Kp = 10.0  # 比例系数
Ki = 2  # 积分系数
Kd = 2  # 微分系数

# 初始化相位差和PID控制器
theta_diff = np.pi / 1.7  # 两个激光器的相位差，初始为pi/3
pid_int = 0.0  # PID控制器的积分项
pid_last_error = 0.0  # PID控制器的上一次误差

# 初始化时间和相位差历史记录
time = [0.0]  # 时间列表
theta_diff_history = [theta_diff]  # 相位差历史记录

# 模拟相位差变化的过程
for i in range(int(t_end / dt)):
    # 计算PID控制器的输出
    error = -theta_diff  # 计算当前误差
    pid_int += error * dt  # 计算积分项
    pid_diff = (error - pid_last_error) / dt  # 计算微分项
    pid_output = Kp * error + Ki * pid_int + Kd * pid_diff  # 计算PID输出
    pid_last_error = error  # 更新上一次误差

    # 更新相位差
    theta_diff += pid_output * dt

    # 记录时间和相位差历史记录
    time.append((i + 1) * dt)
    theta_diff_history.append(theta_diff)

    # 判断是否已经达到了接近0的阈值
    if abs(theta_diff) < 0.001:
        break

# 绘制相位差随时间变化的图像
plt.plot(time, theta_diff_history)
plt.xlabel('Time (s)')
plt.ylabel('Phase Difference (rad)')
plt.title('Phase Difference Control')
plt.savefig('21Release-pi-1.2.pdf')
