import numpy as np
import Circuit as Circuit
import pandas as pd

class Jacobian:

    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.y_bus = np.array(self.circuit.y_bus) #convert y_bus to array
        self.slack: int
        self.pv: int
        self.j_matrix: np.array
        self.j_df: pd.DataFrame
        self.j1 = np.zeros([7, 7])
        self.j2 = np.zeros([7, 7])
        self.j3 = np.zeros([7, 7])
        self.j4 = np.zeros([7, 7])

        self.find_buses()


    def find_buses(self):
        #helper method to sort out buses
        for index, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "slack":
                self.slack = index
            elif bus.bus_type == "pv":
                self.pv= index

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

        self.j_matrix = self.j_matrix.reshape(11,11)
        return self.j_matrix

    def calc_j1(self):

        sum = 0
        # now extract Vk, Vkn, Vn
        for k, bus_k in enumerate(self.circuit.buses.values()):
            for n, bus_n in enumerate(self.circuit.buses.values()):
                    if(k != n):
                        v_k = bus_k.v_pu #get Vk
                        v_n = bus_n.v_pu #get Vn
                        y_kn = np.abs(self.y_bus[k, n]) #get Ykn
                        delta_k = bus_k.delta*np.pi/180 #get delta angle for bus k
                        delta_n = bus_n.delta*np.pi/180 #get delta angle for bus n
                        theta_kn = np.angle(self.y_bus[k, n]) #get theta for kn from Y_bus

                        #add to matrix using partial derivative equation
                        self.j1[k, n] = v_k * y_kn * v_n * np.sin(delta_k - delta_n - theta_kn) #solve equation for partial derivative and add

                    elif (k == n):
                        sum = 0
                        v_k = bus_k.v_pu #get voltage for bus k
                        delta_k = bus_k.delta*np.pi/180 #get angle for bus k
                        for x, bus_x in enumerate(self.circuit.buses.values()):
                            if(x != k): #skip if x = k
                                v_n = bus_x.v_pu  # get Vn
                                y_kn = np.abs(self.y_bus[k, x])  # get Ykn
                                delta_n = bus_x.delta * np.pi / 180  # get delta angle for bus n
                                theta_kn = np.angle(self.y_bus[k, x]) # get theta for kn from Y_bus
                                sum += y_kn * v_n * np.sin(delta_k - delta_n - theta_kn)

                        self.j1[k, k] = -1 * v_k * sum

        self.j1 = np.delete(self.j1, self.slack , axis = 0) #get rid of slack bus row
        self.j1 = np.delete(self.j1, self.slack, axis = 1) #get rid of slack bus column

        return self.j1

    def calc_j2(self):
        # now extract Vk, Vkn, Vn
        for k, bus_k in enumerate(self.circuit.buses.values()):
            for n, bus_n in enumerate(self.circuit.buses.values()):
                if(k != n):
                    v_k = bus_k.v_pu  # get Vk
                    y_kn = np.abs(self.y_bus[k, n])  # get Ykn
                    delta_k = bus_k.delta * np.pi / 180  # get delta angle for bus k
                    delta_n = bus_n.delta * np.pi / 180  # get delta angle for bus n
                    theta_kn = np.angle(self.y_bus[k, n])  # get theta for kn from Y_bus

                    # add to matrix using partial derivative equation
                    self.j2[k, n] = v_k * y_kn * np.cos(delta_k - delta_n - theta_kn)  # solve equation for partial derivative and add

                else:
                    sum = 0
                    delta_k = bus_k.delta*np.pi/180
                    v_k = bus_k.v_pu
                    y_kk = np.abs(self.y_bus[k, k])
                    theta_kk = np.angle(self.y_bus[k, k])

                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        v_n = bus_x.v_pu  # get Vn
                        y_kn = np.abs(self.y_bus[k, x])  # get Ykn
                        delta_n = bus_x.delta * np.pi / 180  # get delta angle for bus n
                        theta_kn = np.angle(self.y_bus[k, x])  # get theta for kn from Y_bus
                        sum += y_kn * v_n * np.cos(delta_k - delta_n - theta_kn)

                    self.j2[k, k] = v_k * y_kk * np.cos(theta_kk) + sum

        self.j2 = np.delete(self.j2, self.slack , axis=0)  # get rid of slack bus row
        self.j2 = np.delete(self.j2, self.slack , axis=1)  # get rid of slack bus col
        self.j2 = np.delete(self.j2, self.pv-1, axis=1)  # get rid of pv column

        return self.j2

    def calc_j3(self):
        # now extract Vk, Vkn, Vn
        for k, bus_k in enumerate(self.circuit.buses.values()):
            for n, bus_n in enumerate(self.circuit.buses.values()):
                if(k != n):
                    v_k = bus_k.v_pu  # get Vk
                    y_kn = np.abs(self.y_bus[k, n])  # get Ykn
                    v_n = bus_n.v_pu #get Vn
                    delta_k = bus_k.delta * np.pi / 180  # get delta angle for bus k
                    delta_n = bus_n.delta * np.pi / 180  # get delta angle for bus n
                    theta_kn = np.angle(self.y_bus[k, n])  # get theta for kn from Y_bus

                    # add to matrix using partial derivative equation
                    self.j3[k, n] = -1 * v_k * y_kn * v_n * np.cos(delta_k - delta_n - theta_kn)  # solve equation for partial derivative and add

                else:
                    sum = 0
                    v_k = bus_k.v_pu  # get voltage for bus k
                    delta_k = bus_k.delta * np.pi / 180  # get angle for bus k
                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        if (x != k):  # skip if x = k
                            v_n = bus_x.v_pu  # get Vn
                            y_kn = np.abs(self.y_bus[k, x])  # get Ykn
                            delta_n = bus_x.delta * np.pi / 180  # get delta angle for bus n
                            theta_kn = np.angle(self.y_bus[k, x])  # get theta for kn from Y_bus
                            sum += y_kn * v_n * np.cos(delta_k - delta_n - theta_kn)

                    self.j3[k, k] = v_k * sum

        self.j3 = np.delete(self.j3, self.slack , axis=0)  # get rid of slack bus row
        self.j3 = np.delete(self.j3, self.slack , axis=1)  # get rid of slack bus col
        self.j3 = np.delete(self.j3, self.pv-1, axis=0)  # get rid of pv row

        return self.j3

    def calc_j4(self):
        # now extract Vk, Vkn, Vn
        for k, bus_k in enumerate(self.circuit.buses.values()):
            for n, bus_n in enumerate(self.circuit.buses.values()):
                if(k != n):
                    v_k = bus_k.v_pu  # get Vk
                    y_kn = np.abs(self.y_bus[k, n])  # get Ykn
                    delta_k = bus_k.delta * np.pi / 180  # get delta angle for bus k
                    delta_n = bus_n.delta * np.pi / 180  # get delta angle for bus n
                    theta_kn = np.angle(self.y_bus[k, n])  # get theta for kn from Y_bus

                    # add to matrix using partial derivative equation
                    self.j4[k, n] = v_k * y_kn * np.sin(delta_k - delta_n - theta_kn)  # solve equation for partial derivative and add

                else:
                    sum = 0
                    delta_k = bus_k.delta * np.pi / 180
                    v_k = bus_k.v_pu
                    y_kk = np.abs(self.y_bus[k, k])
                    theta_kk = np.angle(self.y_bus[k, k])

                    for x, bus_x in enumerate(self.circuit.buses.values()):
                        v_n = bus_x.v_pu  # get Vn
                        y_kn = np.abs(self.y_bus[k, x])  # get Ykn
                        delta_n = bus_x.delta * np.pi / 180  # get delta angle for bus n
                        theta_kn = np.angle(self.y_bus[k, x])  # get theta for kn from Y_bus
                        sum += y_kn * v_n * np.sin(delta_k - delta_n - theta_kn)

                    self.j4[k, k] = -1 * v_k * y_kk * np.sin(theta_kk) + sum

        self.j4 = np.delete(self.j4, self.slack , axis=0)  # get rid of slack bus row
        self.j4 = np.delete(self.j4, self.slack , axis=1)  # get rid of slack bus column
        self.j4 = np.delete(self.j4, self.pv-1, axis=0)   #get rid of pv row
        self.j4 = np.delete(self.j4, self.pv -1 , axis = 1)    # get rid of pv column
        return self.j4


    def print_jacobian(self):
        self.j_df = pd.DataFrame(self.j_matrix, index = ['P Bus 2', 'P Bus 3', 'P Bus 4', 'P Bus 5', 'P Bus 6', 'Q Bus 2', 'Q Bus 3', 'Q Bus 4', 'Q Bus 5', 'Q Bus 6', 'Q Bus 7'], columns = ['Ang Bus 2', 'Ang Bus 3', 'Ang Bus 4', ' Ang Bus 5', ' Ang Bus 6', 'Ang Bus 7', 'Volt Bus 2', 'Volt Bus 3', 'Volt Bus 4', 'Volt Bus 5', 'Volt Bus 6'])
        print("\nJacobian Matrix:")
        print(self.j_df.to_string(float_format=lambda x: f"{x:.5f}"))

