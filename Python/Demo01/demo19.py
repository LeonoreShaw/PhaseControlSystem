import numpy as np
import matplotlib.pyplot as plt

config = {
    "font.family": "serif",  # 使用衬线体
    "font.serif": ["SimSun"],  # 全局默认使用衬线宋体
    "font.size": 14,  # 五号，10.5磅
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",  # 设置 LaTeX 字体，stix 近似于 Times 字体
}


# 设置模拟时间和时间步长
t_end = 20  # 模拟结束时间
dt = 0.001  # 时间步长

# 设置PID参数
Kp = 1.0  # 比例系数
Ki = 0.5  # 积分系数
Kd = 0.1  # 微分系数

# 初始化相位差和PID控制器
theta_diff = np.pi / 3  # 两个激光器的相位差，初始为pi/3
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

# 绘制相位差随时间变化的图像

plt.plot(time, theta_diff_history, label="$ \mathrm{Controlled \; Phase} $")
plt.axhline(y=0, color="r", linestyle="--", label="$ \mathrm{Reference \; Phase} $")
plt.xlabel("Time (s)")
plt.ylabel("Phase Difference (rad)")
plt.title("a Phase Difference Control Demo")
plt.rcParams.update(config)
plt.legend(
    title="\n 比例系数 $K_p$ = 1.0 \n 积分系数 $K_i$ = 0.5 \n 微分系数 $K_d$ = 0.1 \n \n 初始相位差 = $ \dfrac{\pi}{3} $ \n",
    loc="upper right",
)  # 图例
plt.tight_layout()
# plt.savefig('19Release--.pdf')
# plt.savefig('19Release--.pdf')
print(theta_diff)
plt.show()
N