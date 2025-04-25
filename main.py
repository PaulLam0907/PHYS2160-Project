"""
main.py

PHYS2160 Introductory Computational Physics 2024-25 Project
Q2 Driven Oscillation in a Resistive Medium

Written by S. P. Lam
"""

import numpy as np

from ODE2 import ODE2
from Plot import Figure
from Func import Environment
from Diff import dydx

##### CONSTANTS #####
"""
Mass (kg) : m
Damping constant (> 0) (kg/s) : c
Spring constant (N/m) : k  ( larger value = more elastic )
Amplitude of external driving force (N) : F0
Driving frequency : OMEGA_0

Angular frequency : OMEGA = np.sqrt(k/m)
Resonance frequency : OMEGA_R = np.sqrt(OMEGA**2 - (c**2)/2/m**2)
Phase constant : PHI = np.arctan(c*OMEGA_0/(m*((OMEGA**2) - (OMEGA_0**2))))
"""
dataset = {
    "Under-damping": {
        "m"       : 5,
        "c"       : 1.75,
        "k"       : 50,
        "F0"      : 4,
        "OMEGA_0" : 3,
        "dm"      : [1, 2, 3, 4],
        "dc"      : [0.1, 0.5, 1, 1.5, 2, 2.5],
        "dk"      : [50, 70, 90, 110, 130, 150],
        "dF0"     : [1, 2, 3, 4],
        "dOMEGA_0": [1, 2, 3]
    },
    "Critical Damping": {
        "m"      : 5,
        "c"      : 10,
        "k"      : 5,
        "F0"     : 4,
        "OMEGA_0": 0.9
    },
    "Over-damping": {
        "m"      : 5,
        "c"      : 15,
        "k"      : 2,
        "F0"     : 4,
        "OMEGA_0": 3
    }
}

t = np.arange(0, 60, 1e-3)  # time interval
#####################

#### ENVIRONMENT ####
env = Environment(
        m = None,
        c = None,
        k = None,
        F0 = None,
        OMEGA_0 = None,
        OMEGA = "sqrt(k/m)",  # known when k and m are given
        phi = "arctan(c * OMEGA_0 / (m * ((OMEGA**2) - (OMEGA_0**2)) ))"  # known when c , OMEGA_0 , m , k are given
)

# function at steady state of the block
x_s = env.newF(
        "F0*cos(OMEGA_0*t-phi) / sqrt( (m**2)*((OMEGA**2)-(OMEGA_0**2))**2 + (c**2)*(OMEGA_0**2) )",
        "x_s"
)

v_s = env.newF(
        "-F0*OMEGA_0*sin(OMEGA_0*t-phi) / sqrt( (m**2)*((OMEGA**2)-(OMEGA_0**2))**2 + (c**2)*(OMEGA_0**2) )",
        "v_s"
)
#####################


def validate_data(case, c, m, k, OMEGA_0):
    """
    Validate data for different damping condition
    
    :param case: type of damping : "Under-damping", "Critical Damping", "Over-damping"
    :param c: damping constant
    :param m: mass
    :param k: spring constant
    :param OMEGA_0: driving frequency
    :return: bool
    """
    OMEGA = np.sqrt(k/m)
    OMEGA_R = np.sqrt(abs( OMEGA ** 2 - (c ** 2) / 2 / m ** 2 ))
    EPS = np.finfo(float).eps  # https://stackoverflow.com/questions/19141432/python-numpy-machine-epsilon
    
    if case == "Under-damping" and not (c / 2 / m) ** 2 < OMEGA ** 2:
        raise ValueError("Not Under-damping\n"
                         "Condition : (c/2m)^2 < OMEGA^2\n"
                         f"(c/2m)^2 = {(c / 2 / m) ** 2}\n"
                         f"OMEGA^2 = k/m = {OMEGA ** 2}")
    
    elif case == "Critical Damping" and not abs((c / 2 / m) ** 2 - OMEGA ** 2) < EPS:
        raise ValueError("Not Critical Damping\n"
                         "Condition : (c/2m)^2 = OMEGA^2\n"
                         f"(c/2m)^2 = {(c / 2 / m) ** 2}\n"
                         f"OMEGA^2 = k/m = {OMEGA ** 2}")
    
    elif case == "Over-damping" and not (c / 2 / m) ** 2 > OMEGA ** 2:
        raise ValueError("Not Over-damping\n"
                         "Condition : (c/2m)^2 > OMEGA^2\n"
                         f"(c/2m)^2 = {(c / 2 / m) ** 2}\n"
                         f"OMEGA^2 = k/m = {OMEGA ** 2}")
    
    if not OMEGA_0 < OMEGA_R:
        # driving frequency should < resonance frequency
        raise ValueError(f"Driving frequency OMEGA_0 ({OMEGA_0}) should < resonance frequency OMEGA_R ({OMEGA_R})")
    
    return True


def solve_ode2(m, c, k, F0, OMEGA_0, time = np.arange(0, 60, 1e-3)):
    """
    Solving 2nd-order Ordinary Differential Equation
    mx" + cx' + kx = F0*cos(OMEGA_0 * t)
    
    :param m: mass  (kg)
    :param c: damping constant > 0  (kg/s)
    :param k: spring constant  (N/m)
    :param F0: amplitude of external driving force  (N)
    :param OMEGA_0: driving frequency
    # :param OMEGA: angular frequency
    # :param PHI: phase constant
    :param time: time interval of type numpy.array()
    :return: tuple : (displacement x, velocity x')
    """
    # get Environment() class constants
    # assumed env = Environment() class exists
    # this function is dedicatedly written for this project
    _const = env.getConstants()
    
    # set constants
    env.setConstants(
            m = m,
            c = c,
            k = k,
            F0 = F0,
            OMEGA_0 = OMEGA_0,
            # OMEGA = OMEGA,
            # phi = PHI
    )
    
    # compute ODE
    x0 = F0 * np.cos(PHI) + x_s()[0]  # initial condition : x(0)
    x_dot0 = -F0 * (c / (2 * m)) * np.cos(PHI) - F0 * np.sqrt(OMEGA ** 2 - (c / 2 / m) ** 2) * np.sin(-PHI) + v_s()[0]  # -F0*OMEGA_0*np.sin(-PHI) / np.sqrt( (m**2)*((OMEGA**2)-(OMEGA_0**2))**2 + (c**2)*(OMEGA_0**2) )  # initial condition : x'(0)
    ode = ODE2(m, c, k, F0, x0, x_dot0, lambda t: np.cos(OMEGA_0 * t))
    
    # numerical result for 2nd order ODE
    x, v = ode(time)
    
    # replace env constant value to its original
    env.setConstants(_const)
    
    return x, v


##### main #####
for case in ["Under-damping"]:  # dataset.keys():
    data = dataset[case]
    m = data["m"]
    c = data["c"]
    k = data["k"]
    F0 = data["F0"]
    OMEGA_0 = data["OMEGA_0"]
    OMEGA = np.sqrt(k / m)  # angular frequency
    OMEGA_R = np.sqrt(OMEGA ** 2 - (c ** 2) / 2 / m ** 2)  # resonance frequency
    PHI = np.arctan(c * OMEGA_0 / (m * ((OMEGA ** 2) - (OMEGA_0 ** 2))))  # phase constant
    
    # validate data
    validate_data(case, c, m, k, OMEGA_0)
    
    # define and update constant in environment
    env.setConstants(
            m = m,
            c = c,
            k = k,
            F0 = F0,
            OMEGA_0 = OMEGA_0,
            # OMEGA = "sqrt(k/m)",
            # phi = "arctan(c * OMEGA_0 / (m * ((OMEGA**2) - (OMEGA_0**2)) ))"
    )
    
    # Solving 2nd-order Ordinary Differential Equation
    # mx" + cx' + kx = F0*cos(OMEGA_0 * t)
    x, v = solve_ode2(m, c, k, F0, OMEGA_0, t)
    
    ##### graph plotting for PART (A) #####
    f1 = [t, x]
    f2 = [t, x_s(t)]
    
    fig_a = Figure(row = 1, col = 1)
    fig_a.add_graph([f1, f2], label = ["$x(t)$", "$x_s(t)$"])
    fig_a.set_axes_title("Displacement of the Block $x(t)$ and at its Steady State $x_s(t)$")
    fig_a.set_x_label("$t$")
    fig_a.set_y_label("$x(t)$")
    fig_a.plot(tight_layout = False)
    #######################################
    
    ##### graph plotting for PART (B) #####
    g1 = [t, dydx(x, t)]
    g2 = [t, v_s(t)]
    
    fig_b = Figure(row = 1, col = 1)
    fig_b.add_graph([g1, g2], label = ["$v(t)$", "$v_s(t)$"])
    fig_b.set_axes_title("Velocity of the Block $v(t)$ and at its Stead State $v_s(t)$")
    fig_b.set_x_label("$t$")
    fig_b.set_y_label("$v(t)$")
    fig_b.plot(tight_layout = False)
    #######################################
    
    # prepare data for plotting with different values of constants
    dm = data["dm"]
    dc = data["dc"]
    dk = data["dk"]
    dF0 = data["dF0"]
    dOMEGA_0 = data["dOMEGA_0"]
    x_dm = []  # solution for x at different values of m
    x_dc = []  # solution for x at different values of c
    x_dk = []  # solution for x at different values of k
    x_dF0 = []  # solution for x at different values of F0
    x_dOMEGA_0 = []  # solution for x at different values of OMEGA_0
    v_dm = []  # solution for v at different values of m
    v_dc = []  # solution for v at different values of c
    v_dk = []  # solution for v at different values of k
    v_dF0 = []  # solution for v at different values of F0
    v_dOMEGA_0 = []  # solution for v at different values of OMEGA_0
    
    for _m in dm:
        # validate data
        validate_data(case, c, _m, k, OMEGA_0)
        
        # solve ODE
        _x, _v = solve_ode2(_m, c, k, F0, OMEGA_0, t)
        
        # append to data list
        x_dm.append(_x)
        v_dm.append(_v)
        
    for _c in dc:
        # validate data
        validate_data(case, _c, m, k, OMEGA_0)
        
        # solve ODE
        _x, _v = solve_ode2(m, _c, k, F0, OMEGA_0, t)
        
        # append to data list
        x_dc.append(_x)
        v_dc.append(_v)
        
    for _k in dk:
        # validate data
        validate_data(case, c, m, _k, OMEGA_0)
        
        # solve ODE
        _x, _v = solve_ode2(m, c, _k, F0, OMEGA_0, t)
        
        # append to data list
        x_dk.append(_x)
        v_dk.append(_v)
        
    for _F0 in dF0:
        # solve ODE
        _x, _v = solve_ode2(m, c, k, _F0, OMEGA_0, t)
        
        # append to data list
        x_dF0.append(_x)
        v_dF0.append(_v)
        
    for _OMEGA_0 in dOMEGA_0:
        # validate data
        validate_data(case, c, m, k, _OMEGA_0)
        
        # solve ODE
        _x, _v = solve_ode2(m, c, k, F0, _OMEGA_0, t)
        
        # append to data list
        x_dOMEGA_0.append(_x)
        v_dOMEGA_0.append(_v)
        
    
    # repeat plotting with different values of constants
    # varying mass m
    fig_a_dm = Figure(2, 2)
    fig_b_dm = Figure(2, 2)
    
    for i in range(len(dm)):
        # update constant in environment
        env.setConstants(m = dm[i])
        # plot curve
        fig_a_dm.add_graph([[t, x_dm[i]], [t, x_s(t)]], label = ["x(t)", "$x_s(t)$"], index = i + 1)
        fig_a_dm.set_axes_title(f"m = {dm[i]}", index = i + 1)
        fig_b_dm.add_graph([[t, v_dm[i]], [t, v_s(t)]], label = ["v(t)", "$v_s(t)$"], index = i + 1)
        fig_b_dm.set_axes_title(f"m = {dm[i]}", index = i + 1)
        
    fig_a_dm.set_fig_title("Displacement of the Block $x(t)$ at Different Mass $m$")
    fig_a_dm.set_x_label("$t$")
    fig_a_dm.set_y_label("$x(t)$")
    fig_a_dm.plot(h_space = 0.5)
    
    fig_b_dm.set_fig_title("Velocity of the Block $v(t)$ at Different Mass $m$")
    fig_b_dm.set_x_label("$t$")
    fig_b_dm.set_y_label("$v(t)$")
    fig_b_dm.plot(h_space = 0.5)
    
    env.setConstants(m = m)
    
    # varying damping constant c
    fig_a_dc = Figure(3, 2)
    fig_b_dc = Figure(3, 2)
    
    for i in range(len(dc)):
        # update constant in environment
        env.setConstants(c = dc[i])
        # plot curve
        fig_a_dc.add_graph([[t, x_dc[i]], [t, x_s(t)]], label = ["x(t)", "$x_s(t)$"], index = i + 1)
        fig_a_dc.set_axes_title(f"c = {dc[i]}", index = i + 1)
        fig_b_dc.add_graph([[t, v_dc[i]], [t, v_s(t)]], label = ["v(t)", "$v_s(t)$"], index = i + 1)
        fig_b_dc.set_axes_title(f"c = {dc[i]}", index = i + 1)
        
    fig_a_dc.set_fig_title("Displacement of the Block $x(t)$ at Different Damping Constant $c$")
    fig_a_dc.set_x_label("$t$")
    fig_a_dc.set_y_label("$x(t)$")
    fig_a_dc.plot(h_space = 0.5)
    
    fig_b_dc.set_fig_title("Velocity of the Block $v(t)$ at Different Damping Constant $c$")
    fig_b_dc.set_x_label("$t$")
    fig_b_dc.set_y_label("$v(t)$")
    fig_b_dc.plot(h_space = 0.5)
    
    env.setConstants(c = c)
    
    # varying spring constant k
    fig_a_dk = Figure(3, 2)
    fig_b_dk = Figure(3, 2)
    
    for i in range(len(dk)):
        # update constant in environment
        env.setConstants(k = dk[i])
        # plot curve
        fig_a_dk.add_graph([[t, x_dk[i]], [t, x_s(t)]], label = ["x(t)", "$x_s(t)$"], index = i + 1)
        fig_a_dk.set_axes_title(f"k = {dk[i]}", index = i + 1)
        fig_b_dk.add_graph([[t, v_dk[i]], [t, v_s(t)]], label = ["v(t)", "$v_s(t)$"], index = i + 1)
        fig_b_dk.set_axes_title(f"k = {dk[i]}", index = i + 1)
        
    fig_a_dk.set_fig_title("Displacement of the Block $x(t)$ at Different Spring Constant $k$")
    fig_a_dk.set_x_label("$t$")
    fig_a_dk.set_y_label("$x(t)$")
    fig_a_dk.plot(h_space = 0.5)
    
    fig_b_dk.set_fig_title("Velocity of the Block $v(t)$ at Different Spring Constant $k$")
    fig_b_dk.set_x_label("$t$")
    fig_b_dk.set_y_label("$v(t)$")
    fig_b_dk.plot(h_space = 0.5)
    
    env.setConstants(k = k)
    
    # varying driving force F0
    fig_a_dF0 = Figure(2, 2)
    fig_b_dF0 = Figure(2, 2)
    
    for i in range(len(dF0)):
        # update constant in environment
        env.setConstants(F0 = dF0[i])
        # plot curve
        fig_a_dF0.add_graph([[t, x_dF0[i]], [t, x_s(t)]], label = ["x(t)", "$x_s(t)$"], index = i + 1)
        fig_a_dF0.set_axes_title(f"F0 = {dF0[i]}", index = i + 1)
        fig_b_dF0.add_graph([[t, v_dF0[i]], [t, v_s(t)]], label = ["v(t)", "$v_s(t)$"], index = i + 1)
        fig_b_dF0.set_axes_title(f"F0 = {dF0[i]}", index = i + 1)
        
    fig_a_dF0.set_fig_title("Displacement of the Block $x(t)$ at Different Amplitude of Driving Force $F_0$")
    fig_a_dF0.set_x_label("$t$")
    fig_a_dF0.set_y_label("$x(t)$")
    fig_a_dF0.plot(h_space = 0.5)
    
    fig_b_dF0.set_fig_title("Velocity of the Block $v(t)$ at Different Amplitude of Driving Force $F_0$")
    fig_b_dF0.set_x_label("$t$")
    fig_b_dF0.set_y_label("$v(t)$")
    fig_b_dF0.plot(h_space = 0.5)
    
    env.setConstants(F0 = F0)
    
    # varying driving frequency OMEGA_0
    fig_a_dOMEGA_0 = Figure(3, 1)
    fig_b_dOMEGA_0 = Figure(3, 1)
    
    for i in range(len(dOMEGA_0)):
        # update constant in environment
        env.setConstants(OMEGA_0 = dOMEGA_0[i])
        # plot curve
        fig_a_dOMEGA_0.add_graph([[t, x_dOMEGA_0[i]], [t, x_s(t)]], label = ["x(t)", "$x_s(t)$"], index = i + 1)
        fig_a_dOMEGA_0.set_axes_title(f"$\omega_0$ = {dOMEGA_0[i]}", index = i + 1)
        fig_b_dOMEGA_0.add_graph([[t, v_dOMEGA_0[i]], [t, v_s(t)]], label = ["v(t)", "$v_s(t)$"], index = i + 1)
        fig_b_dOMEGA_0.set_axes_title(f"$\omega_0$ = {dOMEGA_0[i]}", index = i + 1)
        
    fig_a_dOMEGA_0.set_fig_title("Displacement of the Block $x(t)$ at Different Driving Frequency $\omega_0$")
    fig_a_dOMEGA_0.set_x_label("$t$")
    fig_a_dOMEGA_0.set_y_label("$x(t)$")
    fig_a_dOMEGA_0.plot(h_space = 0.5)
    
    fig_b_dOMEGA_0.set_fig_title("Velocity of the Block $v(t)$ at Different Driving Frequency $\omega_0$")
    fig_b_dOMEGA_0.set_x_label("$t$")
    fig_b_dOMEGA_0.set_y_label("$v(t)$")
    fig_b_dOMEGA_0.plot(h_space = 0.5)
    
    env.setConstants(OMEGA_0 = OMEGA_0)
    
    
    # prepare data for plotting in PART (C)
    # express x_s as a function of OMEGA_0
    # at different value of c
    # let's consider at constant time t = 2(PI)/OMEGA
    env.setConstants(t = 2 * np.pi / OMEGA)  # add t as constant
    env.popConstants("OMEGA_0")  # remove OMEGA_0 from constants list, take it as variable
    # we can reuse x_s to evaluate amplitude of steady state displacement x_s as a function of OMEGA_0
    # new environment class should be created to avoid confusion and corruption of environment
    
    data = []  # list of graphs' data [[graph1_x, graph1_y], [graph2_x, graph2_y], ...]
    curve_label = []
    X = np.arange(0, 2 * OMEGA_R, 1e-3)  # x-axis value ( OMEGA_0 )
    
    for i in range(5, 75 + 1, 5):
        data.append([
            X,
            x_s(
                    OMEGA_0 = X,
                    c = i / 10
            )
        ])
        curve_label.append(f"$x_s(\omega_0)$ at $c$ = {i / 10}")
    
    ##### graph plotting for PART (c) #####
    fig_c = Figure(row = 1, col = 1)
    fig_c.add_graph(data, label = curve_label)
    fig_c.set_axes_title("Amplitude of Stead-state Displacement $x_s(\omega_0)$ with varying Driving Frequency $\omega_0$ and Damping Constant $c$")
    fig_c.set_x_label("$\omega_0$")
    fig_c.set_y_label("$x_s(\omega_0)$")
    fig_c.set_x_ticks([i * OMEGA for i in range(3)], label = ["0", "$\omega_R$", "2$\omega_R$"])
    fig_c.grid()
    fig_c.plot(tight_layout = False)
    #######################################
    
# end of the program (main.py)
