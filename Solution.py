import numpy as np
import pandas as pd
import Circuit as Circuit
import Jacobian as Jacobian
from typing import Dict, List, Optional
class Solution:

    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.known_power: np.array
        self.power: np.array
        self.mismatch: np.array
        self.jacob = Jacobian.Jacobian(self.circuit)
        self.j_matrix: np.array


    def calc_known_power(self):

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
        self.known_power = np.vstack((P, Q)) / self.circuit.settings.s_base
        return self.known_power

    def get_voltages(self):
        # Extract all per-unit voltages directly from buses
        return np.array([bus.v_pu for bus in self.circuit.buses.values()])

    def calc_injection(self, bus, y_bus, voltages):

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

    def calc_mismatch(self):
        numBuses = len(self.circuit.buses)
        P = np.zeros((numBuses, 1))
        Q = np.zeros((numBuses, 1))

        # Loop through each bus to calculate power injections
        voltages = self.get_voltages()
        for index in range(numBuses):
            busI = f"bus{index + 1}"
            P_k, Q_k = self.calc_injection(busI, self.circuit.y_bus, voltages)
            P[index] = P_k
            Q[index] = Q_k

        # Stack real and reactive power vectors
        self.power = np.vstack((P, Q))
        self.mismatch = self.known_power - self.power

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

        # Convert the filtered list to a numpy array with consistent shape
        temp = np.array(mismatch_filtered)

        # Extract the first and second columns and stack them vertically
        first_column = temp[:, 0]  # First column (index 0)
        second_column = temp[:, 1]  # Second column (index 1)

        # Stack the columns vertically (one on top of the other)
        stacked_array = np.concatenate((first_column, second_column), axis=0)

        # Find the correct index to delete based on the PV bus index.
        # Since slack bus is excluded, adjust the pvIndex to match the correct column in transposed
        for index, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "slack":
                slackIndex = index
            elif bus.bus_type == "pv":
                pvIndex = index

        # Now remove the reactive power mismatch for the PV bus
        # Note: We're dealing with the second row in the transposed array (reactive power)
        index_to_delete = len(self.circuit.buses)-2+pvIndex  # Just delete the reactive power mismatch for the PV bus
        stacked_array = np.delete(stacked_array, index_to_delete)

        # Update self.mismatch to the new transposed array
        self.mismatch = stacked_array
        return self.mismatch

    def calc_jacobian(self):
        self.j_matrix = self.jacob.calc_jacobian()

    def print_jacobian(self):
           self.jacob.print_jacobian()

    def calc_solution(self):
        # Solve for delta x
        delt_x = np.linalg.solve(self.j_matrix, self.mismatch)

        # Separate bus indices based on bus type
        slack_positions = [i for i, bus in self.circuit.buses.items() if bus.bus_type == "slack"]
        pv_positions = [i for i, bus in self.circuit.buses.items() if bus.bus_type == "pv"]

        # Initialize counter and array for new voltage magnitudes
        i = 0
        new_V = np.zeros(len(self.circuit.buses), dtype=complex)

        # Update deltas and voltages for non-slack, non-PV buses
        for idx, bus in self.circuit.buses.items():
            if bus.bus_type != "slack":
                if bus.bus_type != "pv":  # Update voltage for non-slack, non-PV buses
                    bus.set_bus_V(bus.v_pu + delt_x[i])
                bus.set_bus_delta(bus.delta + delt_x[i])
                i += 1

        # Calculate new voltage magnitudes and phases
        for idx, bus in enumerate(self.circuit.buses.values()):  # Use enumerate here
            # Apply magnitude and phase adjustments using delta
            new_V[idx] = bus.v_pu * np.exp(1j * bus.delta)

        return new_V
