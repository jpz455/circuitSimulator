from Circuit import Circuit
from Bus import Bus
import numpy as np

class Solution:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def compute_power_injection(self, bus: Bus, y_bus, voltages: np.array):
        N = bus.numBus
        V_k = voltages[bus.name]
        delta_K = bus.delta
        P_k = 0
        Q_k = 0
        for n in range(N):
            if n != bus.name:
                # Get the admittance element Y_kn from the admittance matrix
                Y_kn = y_bus[bus.name, n]
                # Get the voltage at bus n (complex)
                V_n = voltages[n]
                delta_N = bus.delta[n]  # Assuming delta_N is the angle of voltage at bus n

                # Compute power injection
                P_k += np.abs(V_k) * np.abs(Y_kn) * np.abs(V_n) * np.cos(delta_K - delta_N - np.angle(Y_kn))
                P_k += np.abs(V_k) * np.abs(Y_kn) * np.abs(V_n) * np.sin(delta_K - delta_N - np.angle(Y_kn))
        return P_k, Q_k