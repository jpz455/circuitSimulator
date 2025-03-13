import numpy as np
import Solution as Solution
import Circuit as Circuit
import pandas as pd

class Jacobian:

    def __init__(self, solution: Solution):
        self.solution = solution
        self.circuit = solution.circuit

    def calc_jacobian(self, buses: np.array, ybus: pd.DataFrame, angles: np.array, voltages: np.array):
       #call helper methods to calculate each submatrix
        j1 = self.calc_j1
        j2 = self.calc_j2
        j3 = self.calc_j3
        j4 = self.calc_j4
       #remove unnecessary rows
            #TO DO
        #concatenate into one big matrix
        j_top = np.concatenate(j1, j2)
        j_bottom = np.concatenate(j3, j4)
        j = np.stack(j_top, j_bottom)
        return j

    def calc_j1(self):

        j1 = np.array([14, 14])
        # convert y_bus from dataframe to array
        y_bus = np.array(self.solution.ybus)
        # now extract Vk, Vkn, Vn
        for k, bus_k in enumerate(self.circuit.buses.values()):
            for n, bus_n in enumerate(self.circuit.buses.values()):
                v_k = bus_k.v_pu
                v_n = bus_n.v_pu
                y_kn = np.abs(y_bus[k, n])
                delta_k = bus_k.delta*np.pi/180
                delta_n = bus_n.delta*np.pi/180
                theta_kn = np.angle(y_bus[k, n])

                #add to matrix
                j1[k, n] = v_k*y_kn*v_n*np.sin(delta_k - delta_n - theta_kn)

        return j1

    def calc_j2(self):
        # to do
        j2 = np.array([14, 14])
        return j2

    def calc_j2(self):
        # to do
        j2 = np.array([14, 14])
        return j2

    def calc_j2(self):
        # to do
        j2 = np.array([14, 14])
        return j2

    def calc_off_diag(self):
        #helper method to get inputs for matrix for an iteration

        # first get mismatch matrix for the matrix
        mismatch = self.solution.calcMismatch()



