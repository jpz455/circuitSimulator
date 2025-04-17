from Circuit import Circuit
import numpy as np
import pandas as pd

class Fault:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        circuit.calc_y_bus_positive()
        circuit.calc_y_bus_negative()
        circuit.calc_y_bus_zero()
        self.Z_bus_positive = np.linalg.inv(self.circuit.y_bus_positive)
        self.Z_bus_negative = np.linalg.inv(self.circuit.y_bus_negative)
        self.Z_bus_zero = np.linalg.inv(self.circuit.y_bus_zero)
        self.y_bus_matrix_positive: np.array
        self.y_bus_matrix: np.array
        self.y_bus_matrix_negative: np.array
        self.y_bus_matrix_zero: np.array
        self.fault_voltages_3pb: np.array # 3 phase balanced
        self.fault_voltages_ltl: np.array # line to line
        self.fault_voltages_sltg: np.array # single line to ground
        self.fault_voltages_dltg: np.array # double line to ground
        self.I_ltl: complex
        self.I_3pb: complex
        self.I_sltg: complex
        self.I_dltg: complex


    def calc_z_bus_pos(self, fault_bus: str, fault_v = 1.0):
        slack_y_prime = 0
        pv_y_prime = 0

        # Use subtransient reactance from each generator directly
        for gen in self.circuit.generators.values():
            # Positive sequence
            x_prime_pos = gen.x1
            y_prime_pos = 1 / x_prime_pos if x_prime_pos != 0 else 0  # avoid division by zero

            if gen.bus.bus_type == "slack":
                self.slack_name = gen.bus.name
                slack_y_prime_pos = y_prime_pos
            else:  # assume all others are PV for now
                self.pv_name = gen.bus.name
                pv_y_prime_pos = y_prime_pos

        # Recalculate admittance matrix
        self.circuit.calc_y_bus_positive()
        self.circuit.y_bus_positive.loc[self.slack_name, self.slack_name] += slack_y_prime
        self.circuit.y_bus_positive.loc[self.pv_name, self.pv_name] += pv_y_prime

        # Set pre-fault voltage
        self.circuit.buses[fault_bus].set_bus_V(fault_v)

        # Invert Y bus to get Z bus
        self.y_bus_matrix_positive = np.array(self.circuit.y_bus_positive)
        self.z_bus_positive = np.linalg.inv(self.y_bus_matrix_positive)

        return self.z_bus_positive

    def calc_z_bus_neg(self, fault_bus: str, fault_v = 1.0):
        slack_y_prime = 0
        pv_y_prime = 0

        # Use subtransient reactance from each generator directly
        for gen in self.circuit.generators.values():
            # Positive sequence
            x_prime_neg = gen.x1
            y_prime_neg = 1 / x_prime_neg if x_prime_neg != 0 else 0  # avoid division by zero

            if gen.bus.bus_type == "slack":
                self.slack_name = gen.bus.name
                slack_y_prime_neg = y_prime_neg
            else:  # assume all others are PV for now
                self.pv_name = gen.bus.name
                pv_y_prime_neg = y_prime_neg
        # Recalculate admittance matrix
        self.circuit.calc_y_bus_negative()
        self.circuit.y_bus_negative.loc[self.slack_name, self.slack_name] += slack_y_prime
        self.circuit.y_bus_negative.loc[self.pv_name, self.pv_name] += pv_y_prime

        # Set pre-fault voltage
        self.circuit.buses[fault_bus].set_bus_V(fault_v)

        # Invert Y bus to get Z bus
        self.y_bus_matrix_negative = np.array(self.circuit.y_bus_negative)
        self.z_bus_negative = np.linalg.inv(self.y_bus_matrix_negative)

        return self.z_bus_negative

    def calc_z_bus_zero(self, fault_bus: str, fault_v=1.0):
            slack_y_prime = 0
            pv_y_prime = 0

            # Use subtransient reactance from each generator directly
            for gen in self.circuit.generators.values():
                # Positive sequence
                x_prime_zero = gen.x1
                y_prime_zero = 1 / x_prime_zero if x_prime_zero != 0 else 0  # avoid division by zero

                if gen.bus.bus_type == "slack":
                    self.slack_name = gen.bus.name
                    slack_y_prime_zero = y_prime_zero
                else:  # assume all others are PV for now
                    self.pv_name = gen.bus.name
                    pv_y_prime_zero = y_prime_zero
            # Recalculate admittance matrix
            self.circuit.calc_y_bus_zero()
            self.circuit.y_bus_zero.loc[self.slack_name, self.slack_name] += slack_y_prime
            self.circuit.y_bus_zero.loc[self.pv_name, self.pv_name] += pv_y_prime

            # Set pre-fault voltage
            self.circuit.buses[fault_bus].set_bus_V(fault_v)

            # Invert Y bus to get Z bus
            self.y_bus_matrix_zero = np.array(self.circuit.y_bus_zero)
            self.z_bus_zero = np.linalg.inv(self.y_bus_matrix_zero)

            return self.z_bus_zero

    def calc_3_phase_bal(self, fault_bus: str, fault_v=1.0):
        slack_y_prime = 0
        pv_y_prime = 0

        # Use subtransient reactance from each generator directly
        for gen in self.circuit.generators.values():
            # Use x1 (positive-sequence) or x2 depending on your convention
            x_prime = gen.x1
            y_prime = 1 / x_prime if x_prime != 0 else 0  # avoid division by zero

            if gen.bus.bus_type == "slack":
                self.slack_name = gen.bus.name
                slack_y_prime = y_prime
            else:  # assume all others are PV for now
                self.pv_name = gen.bus.name
                pv_y_prime = y_prime

        # Recalculate admittance matrix
        self.circuit.calc_y_bus_no_gen()
        self.circuit.y_bus.loc[self.slack_name, self.slack_name] += slack_y_prime
        self.circuit.y_bus.loc[self.pv_name, self.pv_name] += pv_y_prime

        # Set pre-fault voltage
        self.circuit.buses[fault_bus].set_bus_V(fault_v)

        # Invert Y bus to get Z bus
        self.y_bus_matrix = np.array(self.circuit.y_bus)
        self.z_bus = np.linalg.inv(self.y_bus_matrix)

        # Get Znn at faulted bus
        index = self.circuit.buses[fault_bus].index - 1
        Znn = self.z_bus[index][index]

        # Subtransient fault current
        self.I_3pb = fault_v / Znn

        # Faulted bus voltages
        self.fault_voltages_3pb = np.empty(len(self.circuit.buses), dtype=np.complex128)
        for k, bus in enumerate(self.circuit.buses.values()):
            self.fault_voltages_3pb[k] = (1 - self.z_bus[k][index] / Znn) * fault_v

        return self.fault_voltages_3pb, self.I_3pb

    def print_fault_voltages(self, study: str):
        if study == '3pb':
            print("Fault Current Magnitude: ", round(np.real(self.I_3pb), 5))
            for i, v in enumerate(self.fault_voltages_3pb):
                print("Bus", i + 1, " voltage magnitude:", round(np.real(v), 5))
        elif study == 'ltl':
            for i, v in enumerate(self.I_ltl):
                print("Fault Current Magnitude: ", round(np.real(self.I_ltl), 5))
            for i, v in enumerate(self.fault_voltages_ltl):
                print("Phase", i, " voltage magnitude:", v)
        elif study == 'sltg':
            for i, v in enumerate(self.I_sltg):
                print("Fault Current Magnitude: ", i)
            for i, v in enumerate(self.fault_voltages_sltg):
                print("Bus", i + 1, " voltage magnitude:", v)
        elif study == 'dltg':
            for i, v in enumerate(self.I_dltg):
                print("Fault Current Magnitude: ", round(np.real(self.I_dltg), 5))
            for i, v in enumerate(self.fault_voltages_dltg):
                print("Bus", i + 1, " voltage magnitude:", round(np.real(v), 5))
        else:
            print("Invalid study type. Try again with 3pb, ltl, sltg, or dltg.")

    def calc_single_line_to_ground(self, fault_bus: str, fault_v = 1.0, z_f = 0.0):
        # Calculate all z buses
        self.Z_bus_positive = self.calc_z_bus_pos(fault_bus, fault_v)
        self.Z_bus_negative = self.calc_z_bus_neg(fault_bus, fault_v)
        self.Z_bus_zero = self.calc_z_bus_zero(fault_bus, fault_v)

        # Get Znn at faulted bus
        index = self.circuit.buses[fault_bus].index - 1
        Znn_pos = self.Z_bus_positive[index][index]
        Znn_neg = self.Z_bus_negative[index][index]
        Znn_zero = self.Z_bus_zero[index][index]

        # Create impedance matrix
        sltg_z = np.zeros([3,3], dtype=np.complex128)
        sltg_z[0][0] = Znn_zero
        sltg_z[1][1] = Znn_pos
        sltg_z[2][2] = Znn_neg

        # connect all sequences in series
        Znn_total = Znn_neg + Znn_pos + Znn_zero + 3*z_f

        # Calculate currents
        Ipos = fault_v/Znn_total
        Ineg = Ipos
        Izero = Ipos

        I = np.zeros([3, 1])
        values = [Izero, Ipos, Ineg]
        I[:, 0] = values

       # Calculate voltages at fault bus
        v = np.zeros([3, 1])
        v[1, 0] = fault_v

        vfb = v - sltg_z*I

        # now get phase voltages
        transform_matrix = np.ones([3, 3])
        a = np.exp(2j*np.pi/3)
        transform_matrix[1][1] = a*a
        transform_matrix[2][2] = a*a
        transform_matrix[2][1] = a
        transform_matrix[1][2] = a

        self.fault_voltages_sltg = transform_matrix*vfb
        self.I_sltg= transform_matrix*I

        return self.fault_voltages_sltg, self.I_sltg

    def calc_line_to_line(self, fault_bus: str):

        return None

    def calc_double_line_to_ground(self, fault_bus: str, Zf=0):

        return None