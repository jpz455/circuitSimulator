import numpy as np
import Circuit as Circuit
import pandas as pd

class Jacobian:

    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.slackI: int = -1
        self.pvI: int = -1
        self.j_matrix: np.array
        self.j_df: pd.DataFrame
        self.size = circuit.buses.__len__() #number of buses in system
        self.j1 = np.zeros([self.size, self.size])
        self.j2 = np.zeros([self.size, self.size])
        self.j3 = np.zeros([self.size, self.size])
        self.j4 = np.zeros([self.size, self.size])

        self.find_buses()
        self.circuit.calc_y_bus_no_gen()
        self.y_bus = np.array(self.circuit.y_bus)


    def find_buses(self):
        #helper method to sort out buses
        for index, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "slack":
                self.slackI = index
            elif bus.bus_type == "pv":
                self.pvI = index


    def calc_jacobian(self):
       #call helper methods to calculate each submatrix
        j1 = self.calc_j1() #6x6 (exclude slack r/c)
        j2 = self.calc_j2() #6x5 (exclude slack r/c, pv c)
        j3 = self.calc_j3() #5x6 (exclude slack r/c, pv r)
        j4 = self.calc_j4() #5x5 (exclude slack r/c, pv r/c)
        self.j_matrix = np.block([[
            [j1, j2],
            [j3, j4]
        ]])

        if len(self.circuit.buses) == 7:
            self.j_matrix = self.j_matrix.reshape(11,11)
        return self.j_matrix

    def calc_j1(self):
        # Initialize the Jacobian matrix of the correct size
        num_buses = len(self.circuit.buses)  # Total number of buses
        self.j1 = np.zeros((num_buses, num_buses))  # Allocate space for the Jacobian matrix

        # Loop over all bus pairs (k, n)
        for k, bus_k in enumerate(self.circuit.buses.values()):
            for n, bus_n in enumerate(self.circuit.buses.values()):
                if k != n:
                    # Extract voltage and Y_bus parameters
                    v_k = bus_k.v_pu  # Voltage for bus k
                    v_n = bus_n.v_pu  # Voltage for bus n
                    y_kn = np.abs(self.y_bus[k, n])  # Y_kn value from Y_bus matrix
                    delta_k = bus_k.delta * np.pi / 180  # Delta angle for bus k (in radians)
                    delta_n = bus_n.delta * np.pi / 180  # Delta angle for bus n (in radians)
                    theta_kn = np.angle(self.y_bus[k, n])  # Theta for kn from Y_bus matrix

                    # Fill the Jacobian matrix using the partial derivative equation
                    self.j1[k, n] = v_k * y_kn * v_n * np.sin(delta_k - delta_n - theta_kn)
                else:
                    # Handle diagonal elements (for bus k == n)
                    sum = 0
                    v_k = bus_k.v_pu  # Voltage for bus k
                    delta_k = bus_k.delta * np.pi / 180  # Delta angle for bus k (in radians)

                    # Sum contributions for diagonal elements
                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        if x != k:
                            v_n = bus_x.v_pu  # Voltage for bus x (not k)
                            y_kn = np.abs(self.y_bus[k, x])  # Y_kn value from Y_bus matrix
                            delta_n = bus_x.delta * np.pi / 180  # Delta angle for bus x (in radians)
                            theta_kn = np.angle(self.y_bus[k, x])  # Theta for kn from Y_bus matrix
                            sum += y_kn * v_n * np.sin(delta_k - delta_n - theta_kn)

                    # Update diagonal element of the Jacobian matrix
                    self.j1[k, k] = -v_k * sum

        # Delete the slack bus row and column
        self.j1 = np.delete(self.j1, self.slackI, axis=0)  # Delete the slack bus row
        self.j1 = np.delete(self.j1, self.slackI, axis=1)  # Delete the slack bus column

        return self.j1

    def calc_j2(self):
        num_buses = len(self.circuit.buses)
        j2 = np.zeros((num_buses, num_buses))
        sum_terms = 0

        for k, bus_k in enumerate(self.circuit.buses.values()):
            delta_k = bus_k.delta * np.pi / 180  # Convert delta_k to radians
            v_k = bus_k.v_pu  # Get Vk
            y_kk = np.abs(self.circuit.y_bus_positive.iloc[k, k])  # Get Ykk
            theta_kk = np.angle(self.circuit.y_bus_positive.iloc[k, k])  # Get theta_kk

            for n, bus_n in enumerate(self.circuit.buses.values()):
                if k != n:
                    y_kn = np.abs(self.circuit.y_bus_positive.iloc[k, n])  # Get Ykn
                    delta_n = bus_n.delta * np.pi / 180  # Convert delta_n to radians
                    theta_kn = np.angle(self.circuit.y_bus_positive.iloc[k, n])  # Get theta_kn

                    # Compute off-diagonal terms
                    j2[k, n] = v_k * y_kn * np.cos(delta_k - delta_n - theta_kn)
                else:
                    sum_terms = 0
                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        v_x = bus_x.v_pu  # Get Vx
                        y_kx = np.abs(self.circuit.y_bus_positive.iloc[k, x])  # Get Ykx
                        delta_x = bus_x.delta * np.pi / 180  # Convert delta_x to radians
                        theta_kx = np.angle(self.circuit.y_bus_positive.iloc[k, x])  # Get theta_kx

                        sum_terms += y_kx * v_x * np.cos(delta_k - delta_x - theta_kx)

                    # Compute diagonal terms
                    j2[k, k] = v_k * y_kk * np.cos(theta_kk) + sum_terms

        # Remove slack bus row/column
        j2 = np.delete(j2, self.slackI, axis=0)
        j2 = np.delete(j2, self.slackI, axis=1)

        # Remove PV bus column
        if self.pvI is not None:
            if self.slackI>self.pvI:
                j2 = np.delete(j2, self.pvI, axis=1)
            else:
                j2 = np.delete(j2, self.pvI - 1, axis=1)

        return j2

    def calc_j3(self):
        # Initialize the Jacobian matrix of the correct size
        num_buses = len(self.circuit.buses)  # Total number of buses
        self.j3 = np.zeros((num_buses, num_buses))  # Allocate space for the Jacobian matrix

        # Iterate over each bus pair (k, n)
        for k, bus_k in enumerate(self.circuit.buses.values()):
            delta_k = bus_k.delta * np.pi / 180  # Convert degrees to radians once
            v_k = bus_k.v_pu  # Per-unit voltage

            for n, bus_n in enumerate(self.circuit.buses.values()):
                if k != n:
                    # Extract necessary values
                    y_kn = np.abs(self.y_bus[k, n])  # Admittance magnitude
                    delta_n = bus_n.delta * np.pi / 180
                    theta_kn = np.angle(self.y_bus[k, n])  # Phase angle

                    # Compute the off-diagonal elements
                    self.j3[k, n] = -v_k * y_kn * np.cos(delta_k - delta_n - theta_kn)

                else:
                    # Compute diagonal elements (sum over all other buses)
                    sum_val = 0
                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        if x != k:
                            v_n = bus_x.v_pu
                            y_kn = np.abs(self.y_bus[k, x])
                            delta_n = bus_x.delta * np.pi / 180
                            theta_kn = np.angle(self.y_bus[k, x])
                            sum_val += y_kn * v_n * np.cos(delta_k - delta_n - theta_kn)

                    self.j3[k, k] = v_k * sum_val

        # Remove slack and PV bus rows/columns
        self.j3 = np.delete(self.j3, self.slackI, axis=0)
        self.j3 = np.delete(self.j3, self.slackI, axis=1)

        # Adjust index after removing slack bus
        if self.slackI > self.pvI:
            self.j3 = np.delete(self.j3, self.pvI, axis=0)  # Remove PV bus row
        else:
            self.j3 = np.delete(self.j3, self.pvI - 1, axis=0)  # Remove PV bus row

        # Return the updated Jacobian matrix
        return self.j3

    def calc_j4(self):
        num_buses = len(self.circuit.buses)
        j4 = np.zeros((num_buses, num_buses))  # Initialize J4 matrix

        for k, bus_k in enumerate(self.circuit.buses.values()):
            delta_k = bus_k.delta * np.pi / 180  # Convert delta_k to radians
            v_k = bus_k.v_pu  # Get Vk
            y_kk = np.abs(self.circuit.y_bus_positive.iloc[k, k])  # Get Ykk
            theta_kk = np.angle(self.circuit.y_bus_positive.iloc[k, k])  # Get theta_kk

            for n, bus_n in enumerate(self.circuit.buses.values()):
                if k != n:
                    y_kn = np.abs(self.circuit.y_bus_positive.iloc[k, n])  # Get Ykn
                    delta_n = bus_n.delta * np.pi / 180  # Convert delta_n to radians
                    theta_kn = np.angle(self.circuit.y_bus_positive.iloc[k, n])  # Get theta_kn

                    # Compute off-diagonal terms
                    j4[k, n] = v_k * y_kn * np.sin(delta_k - delta_n - theta_kn)
                else:
                    sum_terms = 0
                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        v_x = bus_x.v_pu  # Get Vx
                        y_kx = np.abs(self.circuit.y_bus_positive.iloc[k, x])  # Get Ykx
                        delta_x = bus_x.delta * np.pi / 180  # Convert delta_x to radians
                        theta_kx = np.angle(self.circuit.y_bus_positive.iloc[k, x])  # Get theta_kx

                        sum_terms += y_kx * v_x * np.sin(delta_k - delta_x - theta_kx)

                    # Compute diagonal terms
                    j4[k, k] = -1 * v_k * y_kk * np.sin(theta_kk) + sum_terms

        # Remove slack bus row/column
        j4 = np.delete(j4, self.slackI, axis=0)
        j4 = np.delete(j4, self.slackI, axis=1)

        # Remove PV bus column
        if self.slackI > self.pvI:
            j4 = np.delete(j4, self.pvI, axis=0)
            j4 = np.delete(j4, self.pvI, axis=1)
        else:
            # Remove PV bus row/column
            j4 = np.delete(j4, self.pvI - 1, axis=0)
            j4 = np.delete(j4, self.pvI - 1, axis=1)

        return j4



    def print_jacobian(self):
        self.j_df = pd.DataFrame(self.j_matrix, index = ['P Bus 2', 'P Bus 3', 'P Bus 4', 'P Bus 5', 'P Bus 6', 'Q Bus 2', 'Q Bus 3', 'Q Bus 4', 'Q Bus 5', 'Q Bus 6', 'Q Bus 7'], columns = ['Ang Bus 2', 'Ang Bus 3', 'Ang Bus 4', ' Ang Bus 5', ' Ang Bus 6', 'Ang Bus 7', 'Volt Bus 2', 'Volt Bus 3', 'Volt Bus 4', 'Volt Bus 5', 'Volt Bus 6'])
        print("\nJacobian Matrix:")
        print(self.j_df.to_string(float_format=lambda x: f"{x:.5f}"))