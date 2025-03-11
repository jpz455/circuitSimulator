from Circuit import Circuit
from Bus import Bus
import numpy as np

class Solution:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def compute_power_injection(self, bus: Bus, y_bus: np.array, voltages: np.array):
        N = bus.numBus
        V_k = voltages[N-1]  # Complex voltage at bus k
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


    def compute_power_mismatch(self, buses: np.array, y_bus: np.array, voltages: np.array):
        N = buses.numBus
      #empty array to start

        #calculated power
        fxn_real = np.zeros([N-1, 1])
        fxn_reactive = np.zeros([N-1, 1])

        #known power
        y_real = np.zeros([N - 1, 1])
        y_reactive = np.zeros([N - 1, 1])

        for n in buses:
            #calculate power & reactive for all but slack bus
            if buses[n].bus_type != "slack":
                fxn_real[n, 1], fxn_reactive[n, 1] = self.compute_power_injection(buses[n], y_bus[n], voltages)

            #add known values
            if buses[n].bus_type == "pv":
                y_real = self.circuit.generators[n].mw_setpoint
                y_reactive = 0 #tbd
            if buses[n].bus_type == "slack":
                y_real = self.circuit.generators[n].mw_setpoint
                y_reactive = 0 #tbd

        #now stack vectors
        fxn_powers = np.vstack((fxn_real, fxn_reactive))
        y_powers = np.vstack((y_real, y_reactive))

        #subtract
        vec = fxn_powers - y_powers

        return vec

