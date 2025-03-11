from typing import Dict

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
        calc_real = np.zeros([N-1, 1])
        calc_reactive = np.zeros([N-1, 1])

        #known power
        y_real = np.zeros([N - 1, 1])
        y_reactive = np.zeros([N - 1, 1])

        #angle and voltage
        y_ang = np.zeros([N - 1, 1])
        y_v = np.zeros([N - 1, 1])

        for n in buses:
            #calculate power & reactive for all
            calc_real[n, 1], calc_reactive[n, 1] = self.compute_power_injection(buses[n], y_bus[n], voltages)

            #add known values to vectors
            if buses[n].bus_type == "pv":
                #if pv we know power and voltage and angle
                y_ang[n, 1] = self.circuit.buses[n].delta
                y_v[n, 1] = self.circuit.buses[n].v_pu


                # get powers
                y_real[n, 1] = self.circuit.generators[n].mw_setpoint
                # get power factor
                pf = np.cos(self.circuit.buses[n].delta * np.pi / 180)
                # get reactive power
                s = y_real[n, 1] / pf
                y_reactive[n, 1] = s * np.sin(self.circuit.buses[n].delta * np.pi / 180)


            elif buses[n].bus_type == "pq":
                # if pq then we know real and reactive
                y_real[n,1] = self.circuit.generators[n].mw_setpoint
                # get power factor
                pf = np.cos(self.circuit.buses[n].delta*np.pi/180)
                #get reactive power
                s = y_real[n,1]/pf
                y_reactive[n,1]= s*np.sin(self.circuit.buses[n].delta*np.pi/180)

            elif buses[n].bus_type == "slack":
                # if slack we know voltage and angle
                y_ang[n, 1] = self.circuit.buses[n].delta
                y_v[n, 1] = self.circuit.buses[n].v_pu

                # calculate powers
                real_added = 0
                reactive_added = 0
                real_lost = 0
                reactive_lost = 0

                # get all power added to circuit from generators
                for gen in self.circuit.generators:
                    # get real & reactive power associated with generators
                    real_added += self.circuit.generators[gen].mw_setpoint
                    pf = np.cos(self.circuit.generators[gen].bus.delta * np.pi / 180)  # power factor
                    s = self.circuit.generators[gen].mw_setpoint/pf #complex power
                    q = s*np.sin(self.circuit.generators[gen].bus.delta*np.pi/180)
                    reactive_added += q

                # get all power lost in loads
                for load in self.circuit.loads:
                    real_lost += self.circuit.loads[load].real_pwr
                    reactive_lost += self.circuit.loads[load].reactive_pwr


                # sum
                #this is def wrong bc I'm not calculating loss in the power lines
                p_slack = real_added - real_lost
                q_slack = reactive_added - reactive_lost


                y_real[n, 1] = p_slack
                y_reactive[n, 1] = q_slack

        #now stack vectors
        calc_powers = np.vstack((calc_real, calc_reactive))
        y_powers = np.vstack((y_real, y_reactive))

        #subtract
        vec = calc_powers - y_powers

        return vec

