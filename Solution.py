import numpy as np
import pandas as pd
import Circuit as Circuit
import Jacobian as Jacobian
from typing import Dict, List, Optional
import matplotlib.pyplot as plt

class Solution:

    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.known_power: np.array
        self.power: np.array
        self.mismatch: np.array
        self.jacob = Jacobian.Jacobian(self.circuit)
        self.j_matrix: np.array
        self.solutionVect = np.zeros(len(self.circuit.buses) * 2)
        self.j_inv: np.array
        self.slackIndex = self.jacob.slackI
        self.pvIndex = self.jacob.pvI

    def calc_known_power(self):
        P = np.zeros([len(self.circuit.buses), 1])
        Q = np.zeros([len(self.circuit.buses), 1])
        self.knownPQ = np.vstack((P, Q))
        for index, bus in enumerate(self.circuit.buses):
            mismatchKey = "load" + str(index + 1)
            genKey = "Gen " + str(index + 1)
            if mismatchKey in self.circuit.loads:
                print(f"Found {mismatchKey} at bus {bus}")
                self.knownPQ[index] = self.circuit.loads[mismatchKey].real_pwr
                self.knownPQ[index + len(self.circuit.buses)] = self.circuit.loads[mismatchKey].reactive_pwr
            elif genKey in self.circuit.generators and self.circuit.buses["bus" + str(index + 1)].bus_type != "slack":
                print(f"Found {genKey} at bus {self.circuit.generators[genKey].bus.name}")
                bus_name = self.circuit.generators[genKey].bus.name
                bus_index = int(bus_name[3:])
                self.knownPQ[bus_index - 1] = self.circuit.generators[genKey].mw_setpoint
            else:
                print(f"{mismatchKey} does not exist at bus {bus}")
        self.knownPQ = self.knownPQ/self.circuit.settings.s_base
        print("------ known power --------")
        print(self.knownPQ)

    def make_power_mismatch(self):
        calcrealP = np.zeros([len(self.circuit.buses), 1])
        calcreacP = np.zeros([len(self.circuit.buses), 1])
        for tempBus1, bus1 in enumerate(self.circuit.buses.values()):
            tempP = 0
            bus1_vpu = bus1.v_pu
            bus1_delta = bus1.delta
            for tempBus2, bus2 in enumerate(self.circuit.buses.values()):
                y_bus_value = self.circuit.y_bus.loc[f"bus{tempBus1 + 1}", f"bus{tempBus2 + 1}"]
                tempP += np.abs(y_bus_value) * bus2.v_pu * np.cos(bus1_delta - bus2.delta - np.angle(y_bus_value))
            calcrealP[tempBus1] = bus1_vpu * tempP
        for tempBus1Q, bus1Q in enumerate(self.circuit.buses.values()):
            tempQ = 0
            bus1Q_vpu = bus1Q.v_pu
            bus1Q_delta = bus1Q.delta
            for tempBus2Q, bus2Q in enumerate(self.circuit.buses.values()):
                y_bus_value = self.circuit.y_bus.loc[f"bus{tempBus1Q + 1}", f"bus{tempBus2Q + 1}"]
                tempQ += np.abs(y_bus_value) * bus2Q.v_pu * np.sin(bus1Q_delta - bus2Q.delta - np.angle(y_bus_value))
            calcreacP[tempBus1Q] = bus1Q_vpu * tempQ
        self.calcPQ = np.vstack((calcrealP, calcreacP))
        self.mismatch = self.knownPQ - self.calcPQ
        indices_to_delete = []
        # Iterate through mismatch backward
        for index in range(len(self.mismatch) - 1, -1, -1):
            if index > len(self.circuit.buses) - 1:  # If index is in the reactive power part of mismatch
                mismatchIndexTemp = "bus" + str(index - len(self.circuit.buses) + 1)  # Adjust index
                if self.circuit.buses[mismatchIndexTemp].bus_type == "pv":
                    indices_to_delete.append(index)  #mark reactive power of pv bus
            else:
                mismatchIndexTemp = "bus" + str(index + 1)  # Stay in real power index
            if self.circuit.buses[mismatchIndexTemp].bus_type == "slack":
                indices_to_delete.append(index)  #mark slack bus to delete
        self.mismatch = np.delete(self.mismatch, indices_to_delete)
        return self.mismatch

    def make_solution_vector(self):
        bus_keys = sorted(self.circuit.buses.keys(), key=lambda x: int(x[3:]))  #sort buses in order with key lambda
        initD = np.array([[self.circuit.buses[N].delta for N in bus_keys]])
        initV = np.array([[self.circuit.buses[N].v_pu for N in bus_keys]])
        self.initSol = np.hstack((initD, initV))
        indices_to_delete = []
        # Iterate backwards to determine which indices to remove
        for index in range(len(self.circuit.buses) * 2 - 1, -1, -1):
            if index > len(self.circuit.buses) - 1:  # If in reactive power section
                temp = "bus" + str(index - len(self.circuit.buses) + 1)
                if self.circuit.buses[temp].bus_type == "pv":  # Remove PV bus reactive power
                    indices_to_delete.append(index)
            else:  # If in real power section
                temp = "bus" + str(index + 1)
            if self.circuit.buses[temp].bus_type == "slack":  # Remove slack bus contributions
                indices_to_delete.append(index)
        self.initSol = np.delete(self.initSol, indices_to_delete)
        deltaX = np.linalg.solve(self.j_matrix, self.mismatch)
        self.initSol = self.initSol + deltaX
        return self.initSol

    def calc_jacobian(self):
        self.jacob.calc_jacobian()
        self.j_matrix = self.jacob.j_matrix
        return self.j_matrix

    def calc_solution(self):

        tolerance = 0.0001

        #give a max of 50 iterations
        for iterations in range(50):
            mismatchTempI = 0

            #loop through every element of mismatch to check within tolerance
            for mismatchI in range(len(self.mismatch)):

                #get the values from solution vector
                for busIndex in range(len(self.circuit.buses)):


                    if self.circuit.buses["bus" + str(busIndex + 1)].bus_type != "slack" and self.circuit.buses["bus" + str(busIndex + 1)].bus_type != "pv":
                        self.circuit.buses["bus" + str(busIndex + 1)].v_pu = self.initSol[busIndex + len(self.circuit.buses) - 2]
                        self.circuit.buses["bus" + str(busIndex + 1)].delta = self.initSol[busIndex - 1]
                    elif self.circuit.buses["bus" + str(busIndex + 1)].bus_type != "slack":
                        self.circuit.buses["bus" + str(busIndex + 1)].delta = self.initSol[busIndex - 1]

                if np.abs(self.mismatch[mismatchI]) <= tolerance:
                    mismatchTempI += 1


                if mismatchTempI == len(self.mismatch):
                    converged = np.zeros((len(self.circuit.buses), 2))  # Use NumPy for 2D array

                    temp = 0
                    for index in self.circuit.buses:
                        converged[temp, 1] = np.degrees(self.circuit.buses[index].delta)  # Store delta (angle)
                        converged[temp, 0] = self.circuit.buses[index].v_pu  # Store voltage magnitude
                        temp += 1

                    print("Solution found")
                    print("Iteration:", iterations)
                    return converged

            self.calc_jacobian()
            self.make_power_mismatch()
            self.make_solution_vector()


    '''
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
        self.finalVector += 0.00001*self.delta_vec  # Add the correction to the current solution

        # Convert finalVector to 2 arrays for easier indexing
        voltages = np.ones((self.circuit.buses.__len__(), 1))  # array with size of all buses, will skip slack and pv
        deltas = np.zeros((self.circuit.buses.__len__(), 1))  # array with size of all buses, will skip slack
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
            if (k == self.slackIndex):  # if slack bus don't update anything
                continue
            elif (k == self.pvIndex):  # if pv bus update delta only
                bus_k.delta = float(deltas[k])
                continue
            else:
                bus_k.v_pu = float(voltages[k])
                bus_k.delta = float(deltas[k])

        return self.finalVector  # Return the updated solution vector

    def calc_solution(self, tolerance = 0.001):
        data = np.zeros(50) #empty array to hold mismatches to start
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
                # Did not converge
                print("iteration", f, "Mismatches: ", self.mismatch)
                # ~Recursion~
                self.make_solution_vector()
                data[f] = self.mismatch[7]
                if(f == 49):
                    print("did not converge. number of mismatches within tolerance: ", counter)
                    iterations = np.arange(1, 51)
                    plt.figure(figsize=(8, 5))
                    plt.plot(iterations, data, marker='o', color='blue')
                    plt.xlabel('Iteration')
                    plt.ylabel('Mismatch')
                    plt.title('Mismatch vs. Iteration')
                    plt.grid(True)
                    plt.show()
'''