import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def equations(t, y, L, m, k, L1, beta, g):
    theta_1, omega_1, theta_2, omega_2 = y
    gravitational_force = m * g
    elastic_force = k * L1 * (np.sin(theta_2) - np.sin(theta_1))

    temp = theta_1
    theta_1 = omega_1
    omega_1 = (-gravitational_force * L * np.sin(temp) - beta * L * theta_1 + L1 * elastic_force * np.cos(temp)) / (m * L ** 2)

    temp = theta_2
    theta_2 = omega_2
    omega_2 = (-gravitational_force * L * np.sin(temp) - beta * L * theta_2 - L1 * elastic_force * np.cos(temp)) / (m * L ** 2)

    return theta_1, omega_1, theta_2, omega_2

def run_simulation():
    L = float(entry_L.get())
    m = float(entry_m.get())
    k = float(entry_k.get())
    L1 = float(entry_L1.get())
    beta = float(entry_beta.get())
    g = float(entry_g.get())

    if L1 > L:
        print('invalid parametr L1', L1)
        return

    theta1_0 = float(entry_theta1_0.get())
    theta2_0 = float(entry_theta2_0.get())
    omega1_0 = float(entry_omega1_0.get())
    omega2_0 = float(entry_omega2_0.get())

    nat_freq1 = np.sqrt(g / L)
    nat_freq2 = np.sqrt(g / L + 2 * k * L1 ** 2 / (m * L ** 2))

    print('FIRST NATURAL FREQ: ', nat_freq1)
    print('SECOND NATURAL FREQ: ', nat_freq2)

    t_span = (0, float(entry_timespan.get()))
    t_eval = np.linspace(t_span[0], t_span[1], 1000)
    y0 = [theta1_0, omega1_0, theta2_0, omega2_0]

    sol = solve_ivp(equations, t_span, y0, args=(L, m, k, L1, beta, g), t_eval=t_eval)

    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(sol.t, sol.y[0], label='Угол θ1')
    plt.plot(sol.t, sol.y[2], label='Угол θ2')
    plt.legend()
    plt.xlabel('Время (с)')
    plt.ylabel('Углы (рад)')
    plt.title('Зависимость углов от времени')

    plt.subplot(2, 1, 2)
    plt.plot(sol.t, sol.y[1], label='Угловая скорость ω1')
    plt.plot(sol.t, sol.y[3], label='Угловая скорость ω2')
    plt.legend()
    plt.xlabel('Время (с)')
    plt.ylabel('Угловые скорости (рад/с)')
    plt.title('Зависимость угловых скоростей от времени')

    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Параметры маятника")

fields = [
    ("длина маятника L", "1.0"),
    ("масса грузов m", "1.0"),
    ("коэффициент жесткости пружины k", "1.0"),
    ("расстояние пружины от подвеса L1", "0.5"),
    ("коэффициент затухания beta", "0.1"),
    ("ускорение свободного падения g", "9.81"),
    ("угол отклонения 1 маятника phi1_0", "0"),
    ("угол отклонения 2 маятника phi2_0", "1"),
    ("начальная скорость 1 маятника omega1_0", "0.0"),
    ("начальная скорость 2 маятника omega2_0", "0.0"),
    ("время симуляции timespan", "10.0")
]

entries = {}
for field, default in fields:
    frame = tk.Frame(root)
    label = tk.Label(frame, text=field)
    entry = tk.Entry(frame)
    entry.insert(0, default)
    label.pack(side="left")
    entry.pack(side="right")
    frame.pack(fill="x", padx=10, pady=5)
    entries[field] = entry

entry_L = entries["длина маятника L"]
entry_m = entries["масса грузов m"]
entry_k = entries["коэффициент жесткости пружины k"]
entry_L1 = entries["расстояние пружины от подвеса L1"]
entry_beta = entries["коэффициент затухания beta"]
entry_g = entries["ускорение свободного падения g"]
entry_theta1_0 = entries["угол отклонения 1 маятника phi1_0"]
entry_theta2_0 = entries["угол отклонения 2 маятника phi2_0"]
entry_omega1_0 = entries["начальная скорость 1 маятника omega1_0"]
entry_omega2_0 = entries["начальная скорость 2 маятника omega2_0"]
entry_timespan = entries["время симуляции timespan"]

button = ttk.Button(root, text="Запустить симуляцию", command=run_simulation)
button.pack(pady=20)

root.mainloop()
