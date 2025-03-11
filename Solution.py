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
        P_k = 0 #np.zeros([N,1])
        Q_k = 0 #p.zeros([N,1])

        # get buses as list
        bus_list = list(self.circuit.buses.items())
        bus_values = [value for key, value in bus_list]

        for n in range(N):
            #get bus name for column index in y_bus
            bus_n = bus_values[n]
            if bus_n.name != bus.name:
                # Get the admittance element Y_kn
                Y_kn = y_bus.loc[bus.name, bus_n.name]
                # Get the voltage at bus n
                V_n = voltages[n-1]
                delta_N = np.angle(V_n)  # Extract angle from complex voltage

                # Compute active and reactive power injections
                P_k += np.abs(V_k) * np.abs(Y_kn) * np.abs(V_n) * np.cos(delta_K - delta_N - np.angle(Y_kn))
                Q_k += np.abs(V_k) * np.abs(Y_kn) * np.abs(V_n) * np.sin(delta_K - delta_N - np.angle(Y_kn))

        return P_k, Q_k


    def compute_power_mismatch(self, buses: np.array, y_bus: np.array, voltages: np.array):
        size = 0
        for bus in buses:
           size += 1

        N = size
      #empty array to start
        calc_real = np.array([])
        calc_reactive =np.array([])
        #known power
        y_real = np.zeros([N, 1])
        y_reactive = np.zeros([N, 1])

        #angle and voltage
        y_ang = np.zeros([N, 1])
        y_v = np.zeros([N, 1])

        # set index for array at 0 to start
        i = 0
        for n in range(N):
            real, reactive = self.compute_power_injection(buses[i], y_bus, voltages)
            calc_real = np.append(calc_real, real)
            calc_reactive = np.append(calc_reactive, reactive)
            i +=1

        #rotate array
        calc_real = calc_real.reshape(-1, 1)
        calc_reactive = calc_reactive.reshape(-1, 1)

        index = 0
        for n in buses:
            #add known values to vectors
            if buses[index].bus_type == "pv":
                #if pv we know power and voltage and angle
                y_ang[index, 1] = self.circuit.buses[n].delta
                y_v[index, 1] = self.circuit.buses[n].v_pu


                # get powers
                y_real[index, 1] = self.circuit.generators[n].mw_setpoint
                # get power factor
                pf = np.cos(self.circuit.buses[n].delta * np.pi / 180)
                # get reactive power
                s = y_real[n, 1] / pf
                y_reactive[n, 1] = s * np.sin(self.circuit.buses[n].delta * np.pi / 180)


            elif buses[index].bus_type == "pq":
                # if pq then we know real and reactive
                y_real[index, 1] = self.circuit.generators[n].mw_setpoint
                # get power factor
                pf = np.cos(self.circuit.buses[n].delta*np.pi/180)
                #get reactive power
                s = y_real[index, 1]/pf
                y_reactive[index, 1]= s*np.sin(self.circuit.buses[n].delta*np.pi/180)

            elif buses[index].bus_type == "slack":
                # if slack we know voltage and angle
                y_ang[index, 1] = self.circuit.buses[n].delta
                y_v[index, 1] = self.circuit.buses[n].v_pu

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

            #increment index
            index += 1

        #now stack vectors
        calc_powers = np.vstack((calc_real, calc_reactive))
        y_powers = np.vstack((y_real, y_reactive))
        #subtract
        vec = calc_powers - y_powers

        return vec

