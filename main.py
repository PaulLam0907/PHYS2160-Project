"""
main.py

Written by S. P. Lam
"""

import numpy as np

from ODE2 import ODE2
from Plot import Plot
from Func import Func
from Diff import dydx

##### CONSTANTS #####
m = 5  # mass
c = 3  # damping constant > 0
k = 75  # spring constant
F0 = 2  # amplitude of external driving force
OMEGA0 = 2  # driving frequency
OMEGA = np.sqrt(k/m)  # angular frequency
PHI = np.arctan(c*OMEGA0/(m*((OMEGA**2) - (OMEGA0**2))))  # phase constant
#####################

# Solving 2nd-order Ordinary Differential Equation
# mx" + cx' + kx = F0*cos(OMEGA0 * t)
x0 = F0  # initial condition : x(0)
x_dot0 = -F0*OMEGA0*np.sin(-PHI) / np.sqrt( (m**2)*((OMEGA**2)-(OMEGA0**2))**2 + (c**2)*(OMEGA0**2) )  # initial condition : x'(0)
ode = ODE2(m, c, k, F0, x0, x_dot0, lambda t: np.cos(OMEGA0*t))

# numerical result for 2nd order ODE
t = np.arange(0, 60, 1e-3)
x, v = ode(t)

# at steady state
x_s_ = Func(
        "F0*cos(OMEGA0*t-phi) / sqrt( (m**2)*((OMEGA**2)-(OMEGA0**2))**2 + (c**2)*(OMEGA0**2) )",
        F0 = F0,
        OMEGA0 = OMEGA0,
        OMEGA = OMEGA,
        m = m,
        c = c,
        phi = PHI
)
x_s = x_s_(t)

v_s_ = Func(
        "-F0*OMEGA*sin(OMEGA0*t-phi) / sqrt( (m**2)*((OMEGA**2)-(OMEGA0**2))**2 + (c**2)*(OMEGA0**2) )",
        F0 = F0,
        OMEGA0 = OMEGA0,
        OMEGA = OMEGA,
        m = m,
        c = c,
        phi = PHI
)
v_s = v_s_(t)


# graph plotting for PART (A)
f1 = [t, x]
f2 = [t, x_s]
Plot(
        [f1, f2],
        curve_label = ["$x(t)$", "$x_s(t)$"],
        title = "Displacement of the Block $x(t)$ and at its Steady State $x_s(t)$",
        x_label = "$t$",
        y_label = "$x(t)$"
)


# graph plotting for PART (B)
# g0 = [t, v]
g1 = [t, dydx(x, t)]
g2 = [t, v_s]
Plot(
        [g1, g2],
        curve_label = ["$v(t)$", "$v_s(t)$"],
        title = "Velocity of the Block $v(t)$ and at its Stead State $v_s(t)$",
        x_label = "$t$",
        y_label = "$v(t)$"
)


# express x_s as a function of OMEGA0
# at constant time t = 2(PI)/OMEGA
# at different value of c
x_s0 = Func(  # amplitude of steady state displacement
        "F0*cos(OMEGA0*t-phi) / sqrt( (m**2)*((OMEGA**2)-(OMEGA0**2))**2 + (c**2)*(OMEGA0**2) )",
        F0 = F0,
        OMEGA = OMEGA,
        t = 2*np.pi/OMEGA,
        m = m,
        phi = PHI
)

# preparing data for plotting
data = []  # list of graphs' data [[graph1_x, graph1_y], [graph2_x, graph2_y], ...]
curve_label = []
X = np.arange(0, 2*OMEGA)  # x-axis value

for c in range(1, 75+1, 5):
    data.append([
        X,
        x_s0(
                OMEGA0 = X,
                c = c/10
        )
    ])
    curve_label.append(f"$x_s(\omega_0)$ at $c$ = {c/10}")


# graph plotting for PART (C)
Plot(
        data,
        curve_label = curve_label,
        title = "Amplitude of Stead-state Displacement $x_s(\omega_0)$ with varying Driving Frequency $\omega_0$ and Damping Constant $c$",
        x_label = "$\omega_0$",
        y_label = "$x_s(\omega_0)$"
)
