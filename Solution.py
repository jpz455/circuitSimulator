from Circuit import Circuit
from Bus import Bus
import numpy as np

class Solution:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def compute_power_injection(self, bus: Bus, y_bus: np.array, voltages: np.array):
        N = bus.numBus
        V_k = voltages[bus.name]  # Complex voltage at bus k
        delta_K = np.angle(V_k)   # Extract angle from complex voltage
        P_k = np.zeros([N,1])
        Q_k = np.zeros([N,1])


        for n in range(N):
            if n != bus.name:
                # Get the admittance element Y_kn
                Y_kn = y_bus[bus.name, n]
                # Get the voltage at bus n
                V_n = voltages[n]
                delta_N = np.angle(V_n)  # Extract angle from complex voltage

                # Compute active and reactive power injections
                P_k += np.abs(V_k) * np.abs(Y_kn) * np.abs(V_n) * np.cos(delta_K - delta_N - np.angle(Y_kn))
                Q_k += np.abs(V_k) * np.abs(Y_kn) * np.abs(V_n) * np.sin(delta_K - delta_N - np.angle(Y_kn))

        return P_k, Q_k
