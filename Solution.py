import numpy as np
import Circuit as Circuit

class Solution:

    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def calcKnownPower(self):

        n = len(self.circuit.buses)
        P = np.zeros((n, 1))
        Q = np.zeros((n, 1))

        # Loop through all buses and assign real/reactive power
        for i, bus in enumerate(self.circuit.buses):
            # Real Power (P)
            load = self.circuit.loads.get(bus)
            generator = self.circuit.generators.get(bus)

            if load:
                P[i] = load.real_pwr
            if generator:
                P[i] += generator.mw_setpoint  # Add generator contribution

            # Reactive Power (Q)
            if load:
                Q[i] = load.reactive_pwr

        # Stack real and reactive power vectors and convert to per-unit
        self.knownPower = np.vstack((P, Q)) / self.circuit.settings.s_base
        return self.knownPower

    def get_voltages(self):
        # Extract all per-unit voltages directly from buses
        return np.array([bus.v_pu for bus in self.circuit.buses.values()])

    def calcInjection(self, bus, y_bus, voltages):

        bus_index = self.circuit.buses[bus]  # Access the bus object
        N = bus_index.numBus - 1  # Ensure correct index

        V_k = voltages[N]  # Complex voltage at bus k
        delta_K = np.angle(V_k)
        P_k, Q_k = 0, 0

        # Precompute absolute value of V_k for reuse in the loop
        abs_V_k = np.abs(V_k)

        for n, bus_n in enumerate(self.circuit.buses.values()):
            Y_kn = y_bus.loc[bus_index.name, bus_n.name]
            V_n = voltages[n]
            delta_N = np.angle(V_n)
            abs_V_n = np.abs(V_n)
            abs_Y_kn = np.abs(Y_kn)

            # Compute active and reactive power
            delta_diff = delta_K - delta_N - np.angle(Y_kn)
            P_k += abs_V_k * abs_Y_kn * abs_V_n * np.cos(delta_diff)
            Q_k += abs_V_k * abs_Y_kn * abs_V_n * np.sin(delta_diff)

        return P_k, Q_k

    def calcMismatch(self):
        numBuses = len(self.circuit.buses)
        P = np.zeros((numBuses, 1))
        Q = np.zeros((numBuses, 1))

        # Loop through each bus to calculate power injections
        voltages = self.get_voltages()
        for index in range(numBuses):
            busI = f"bus{index + 1}"
            P_k, Q_k = self.calcInjection(busI, self.circuit.y_bus, voltages)
            P[index] = P_k
            Q[index] = Q_k

        # Stack real and reactive power vectors
        self.power = np.vstack((P, Q))
        self.mismatch = self.knownPower - self.power

        # Create a list to hold the filtered mismatches
        mismatch_filtered = []

        for iteration, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "pv":
                # Exclude only the reactive power mismatch for PV buses, keep real power mismatch
                mismatch_filtered.append([self.mismatch[iteration][0], 0])  # Set Q mismatch to 0 for PV buses
            elif bus.bus_type != "slack":
                # Include real and reactive power mismatches for non-PV, non-slack buses
                mismatch_filtered.append(
                    [self.mismatch[iteration][0], self.mismatch[iteration + numBuses][0]])  # Separate real and reactive

        # Convert the filtered list to a numpy array with consistent shape
        self.mismatch = np.array(mismatch_filtered)

        return self.mismatch
