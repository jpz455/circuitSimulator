import numpy as np
import pandas as pd
import Circuit as Circuit
import Jacobian as Jacobian
from typing import Dict, List, Optional
import matplotlib.pyplot as plt



class Solution:

    def __init__(self, circuit: Circuit, mode: str):
        self.mode = mode
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
        self.slack_index: int
        self.pv_index: int


    def change_mode(self, mode: str):
        self.mode = mode

    def run_solver(self):
        if(self.mode == "power flow"):
            self.make_solution_vector()
            self.calc_solution()
        elif(self.mode == "fault analysis"):
            #fault_bus = input("Add fault bus: ")
            fault_bus = "bus3"
            st_x = [0.05j, 0.05j]
            #st_x[0] = input("Add slack generator subtransient reactance: ")
            #st_x[1] = input("Add second generator subtransient reactance: ")
            self.calc_fault_study(fault_bus, st_x)
            self.print_fault_voltages()
            print("Fault current at bus", fault_bus, ": ", self.Ifn)

        else:
            print("Invalid mode.")
            self.mode = input("Select a mode: Type fault analysis or power flow:")
            self.run_solver()


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



    def print_jacobian(self):
           self.jacob.print_jacobian()



    def calc_fault_study(self, fault_bus: str, subtrans_x: [], fault_v = 1.0):

        # Add subtransient reactance to generators
        for k, gen in enumerate(self.circuit.generators.values()):
            gen.set_subtransient_x(subtrans_x[k])
            if gen.bus.bus_type == "slack": #if it's the slack generator
                self.slack_name = gen.bus.name # save slack bus name
                slack_x_prime = gen.subtransient_x # save x"
                slack_y_prime = 1/slack_x_prime # convert to y"
            else: #it's a pv generator
                self.pv_name = gen.bus.name # save pv bus name
                pv_x_prime = gen.subtransient_x # save x"
                pv_y_prime = 1/pv_x_prime # convert to y"

        # modify y bus
        self.circuit.calc_y_bus()
        #only have to modify diagonals
        self.circuit.y_bus.loc[self.slack_name, self.slack_name] += slack_y_prime
        self.circuit.y_bus.loc[self.pv_name, self.pv_name] += pv_y_prime

        # Set pre-fault voltage
        self.circuit.buses[fault_bus].set_bus_V(fault_v)  # set the bus to fault with voltage given or default 1

        # Convert y_bus to z_bus
        self.y_bus_matrix = np.array(self.circuit.y_bus)
        self.z_bus = np.linalg.inv(self.y_bus_matrix)

        # Get Znn
        index = self.circuit.buses[fault_bus].index - 1 # get index
        Znn = self.z_bus[index][index]

        # subtransient fault current at that bus
        self.Ifn = fault_v/Znn

        # Calculate bus voltages
        self.fault_voltages = np.empty(len(self.circuit.buses), dtype=np.complex128) # initialize array
        for k, bus in enumerate(self.circuit.buses.values()): #calculate voltages
            self.fault_voltages[k] = (1 - self.z_bus[k][index]/Znn) * fault_v

        return self.fault_voltages, self.Ifn

    def print_fault_voltages(self):
        for i, v in enumerate(self.fault_voltages):
            print("Bus", i + 1, " voltage:", round(np.real(v), 5))
            print("Bus", i + 1, " angle:", round(np.imag(v) * 180/np.pi, 5))

