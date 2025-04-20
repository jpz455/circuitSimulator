import numpy as np
import Circuit as Circuit
import Jacobian as Jacobian
import pandas as pd

class Solution:

    def __init__(self, circuit: Circuit):

        self.circuit = circuit
        self.known_power: np.array
        self.power: np.array
        self.mismatch: np.array
        self.jacob = Jacobian.Jacobian(self.circuit)
        self.j_matrix: np.array
        self.solutionVect = np.zeros(len(self.circuit.buses) * 2)
        self.calcPQ = np.array
        self.knownPQ = np.array
        self.initSol = np.array
        self.slack_name: str
        self.pv_name: str




    def calc_known_power(self):
        P = np.zeros([len(self.circuit.buses), 1])
        Q = np.zeros([len(self.circuit.buses), 1])
        self.knownPQ = np.vstack((P, Q))
        for index, bus in enumerate(self.circuit.buses):
            mismatchKey = "load" + str(index + 1)
            genKey = "Gen " + str(index + 1)
            if mismatchKey in self.circuit.loads:
                #print(f"Found {mismatchKey} at bus {bus}")
                self.knownPQ[index] = self.circuit.loads[mismatchKey].real_pwr
                self.knownPQ[index + len(self.circuit.buses)] = self.circuit.loads[mismatchKey].reactive_pwr
            elif genKey in self.circuit.generators and self.circuit.buses["bus" + str(index + 1)].bus_type != "slack":
                #print(f"Found {genKey} at bus {self.circuit.generators[genKey].bus.name}")
                bus_name = self.circuit.generators[genKey].bus.name
                bus_index = int(bus_name[3:])
                self.knownPQ[bus_index - 1] = self.circuit.generators[genKey].mw_setpoint

        self.knownPQ = self.knownPQ/self.circuit.settings.s_base
        return self.knownPQ
        #print("------ known power --------")
        #print(self.knownPQ)

    def calc_mismatch(self):
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

    def calc_solutionRef(self):
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
        max_iter = 50



        for iterations in range(max_iter):
            self.calc_jacobian()
            self.calc_mismatch()

            if np.all(np.abs(self.mismatch) <= tolerance):
                break

            deltaX = np.linalg.solve(self.j_matrix, self.mismatch)
            self.initSol = self.initSol + deltaX

            # Update bus voltages and angles
            for busIndex, (bus_name, bus) in enumerate(self.circuit.buses.items()):
                if bus.bus_type == "pq":
                    bus.v_pu = self.initSol[busIndex + len(self.circuit.buses) - 2]
                    bus.delta = self.initSol[busIndex - 1]
                elif bus.bus_type == "pv":
                    bus.delta = self.initSol[busIndex - 1]

        # Package final converged values
        converged = np.zeros((len(self.circuit.buses), 2))
        for i, bus in enumerate(self.circuit.buses.values()):
            converged[i, 0] = bus.v_pu
            converged[i, 1] = np.degrees(bus.delta)

        return converged, iterations + 1

    def print_jacobian(self):
           self.jacob.print_jacobian()



