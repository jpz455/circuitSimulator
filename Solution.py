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
        self.find_buses()
        self.solutionVect = np.zeros(len(self.circuit.buses) * 2)
        self.j_inv: np.array
        self.slackIndex = self.jacob.slackI
        self.pvIndex = self.jacob.pvI

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
        index_to_delete = len(self.circuit.buses)-2 + pvIndex  # Just delete the reactive power mismatch for the PV bus
        stacked_array = np.delete(stacked_array, index_to_delete)

        # Update self.mismatch to the new transposed array
        self.mismatch = stacked_array
        return self.mismatch

    def calc_jacobian(self):
        self.jacob.calc_jacobian()
        self.j_matrix = self.jacob.j_matrix
        return self.j_matrix

    def print_jacobian(self):
           self.jacob.print_jacobian()

    def find_buses(self):
        #helper method to sort out buses
        for index, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "slack":
                self.slackIndex = index
            elif bus.bus_type == "pv":
                self.pvIndex = index

    def make_solution_vector(self):
        #get j_matrix and mismatch
        self.j_matrix = self.calc_jacobian()
        self.mismatch = self.calc_mismatch()

        # Initialize delta and V with appropriate sizes
        delta = np.zeros(len(self.circuit.buses))  # Exclude slack bus from delta
        V = np.ones(len(self.circuit.buses))  # Exclude slack and PV bus from V

        # Set voltage magnitudes for each bus (excluding slack and PV bus)
        voltageIndex = 0
        for bus_k in self.circuit.buses.values():
                V[voltageIndex] = bus_k.v_pu
                voltageIndex += 1  # Increment the index for V

        # Set voltage angles for each bus (excluding slack bus only)
        deltaIndex = 0
        for bus_j in self.circuit.buses.values():
            delta[deltaIndex] = bus_j.delta
            deltaIndex += 1  # Increment the index for delta

        # Get rid of slack bus and PV bus voltage
        V = np.delete(V, self.slackIndex)  # Delete slack bus column
        V = np.delete(V, self.pvIndex - 1) # Delete PV bus column; has shifted over 1 due to deletion

       #Get rid of slack bus delta
        delta = np.delete(delta, self.slackIndex) # Delete slack bus column

        # Combine the delta and V vectors into a single solution vector
        self.finalVector = np.hstack((delta, V))  # Stack delta and V horizontally

        # Solve for the correction using the mismatch
        self.j_inv = np.linalg.inv(self.j_matrix) #invert jacobian
        self.delta_vec = np.linalg.matmul(self.j_inv, self.mismatch)  # Solve for the correction vector
        # Update the solution vector with the correction
        self.finalVector += self.delta_vec  # Add the correction to the current solution
        return self.finalVector  # Return the updated solution vector

    def calc_solution(self, tolerance = 0.001):
        # Tolerance for convergence
        tolerance = tolerance # Update tolerance if user provided otherwise default = 0.001
        for f in range(50):  # Maximum number of iterations
            counter = 0  # To count how many mismatch values are within tolerance

            for mismatchIndex in range(len(self.mismatch)):
                # Check if mismatch for the current bus is within tolerance
                if np.abs(self.mismatch[mismatchIndex]) <= tolerance:
                    counter += 1

            # If all mismatches are within tolerance, we've converged
            if counter == len(self.mismatch):
                a = 0
                # Populate the solution vector with delta and v_pu for each bus
                for bus_k in self.circuit.buses.values():
                    if bus_k != self.circuit.buses[f"bus{self.slackIndex + 1}"]:  # Skip slack bus
                        self.solutionVect[a] = bus_k.delta  # Set delta (voltage angle)
                        self.solutionVect[a + len(self.circuit.buses)] = bus_k.v_pu  # Set v_pu (voltage magnitude)
                        a += 1

                # Print the converged solution
                print("Converged solution:", self.solutionVect)
                return self.solutionVect  # Return the solution vector
            else:
                # If not converged, update all buses
                # Convert solutionVect to 2 arrays for easier indexing
                voltages = np.ones((self.circuit.buses.__len__(), 1)) # array with size of all buses, will skip slack and pv
                deltas = np.zeros((self.circuit.buses.__len__(), 1)) # array with size of all buses, will skip slack
                # set up indices
                v_ind = 0
                d_ind = 0
                # Copy over voltages
                while (v_ind < len(voltages)):
                    if (v_ind != self.slackIndex and v_ind != self.slackIndex):
                        voltages[v_ind] = self.finalVector[v_ind]
                    v_ind += 1
                # Copy over deltas
                while (d_ind < len(deltas)):
                    if (d_ind != self.slackIndex):
                        deltas[d_ind] = self.finalVector[d_ind]
                    d_ind += 1

               # Now update buses in Circuit
                for k, bus_k in enumerate(self.circuit.buses.values()):
                    if(k == self.slackIndex): # if slack bus don't update anything
                        continue
                    elif(k == self.pvIndex): # if pv bus update delta only
                        bus_k.delta = deltas[k]
                        continue
                    else:
                        bus_k.v_pu = voltages[k]
                        bus_k.delta = deltas[k]

                print("iteration", f, "Mismatches: ", self.mismatch)
                # ~Recursion~
                self.make_solution_vector()

                if(f == 49):
                    print("did not converge. number of mismatches within tolerance: ", counter)









