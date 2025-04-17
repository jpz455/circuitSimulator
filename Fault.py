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
        # 3 phase balanced
        if study == '3pb':
            print("Fault Current Magnitude: ", round(np.real(self.I_3pb), 5))
            for i, v in enumerate(self.fault_voltages_3pb):
                print("Bus", i + 1, " voltage magnitude:", round(np.real(v), 5))

        # line to line
        elif study == 'ltl':
            print(self.fault_voltages_ltl, self.I_ltl)

        # single line to ground
        elif study == 'sltg':
            for phase, i in enumerate(self.I_sltg):
                print("Phase:", phase, " Current: ", i)
            for phase, v in enumerate(self.fault_voltages_sltg):
                print("Phase", phase, " voltage magnitude:", v)

        # double line to ground
        elif study == 'dltg':
            print(self.fault_voltages_dltg, self.I_dltg)

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

        I = np.empty([3, 1], dtype=np.complex128)
        I[0, 0] = Izero
        I[1, 0] = Ipos
        I[2, 0] = Ineg

       # Calculate voltages at fault bus
        v = np.zeros([3, 1])
        v[1, 0] = fault_v


        vfb = v - np.matmul(sltg_z, I)

        # now get phase voltages
        transform_matrix = np.ones([3, 3], dtype = np.complex128)
        a = np.exp(2j*np.pi/3)
        transform_matrix[1][1] = a*a
        transform_matrix[2][2] = a*a
        transform_matrix[2][1] = a
        transform_matrix[1][2] = a

        self.fault_voltages_sltg = np.matmul(transform_matrix, vfb) # 3x3 times 3x1 = 3x1
        self.I_sltg= np.matmul(transform_matrix, I)

        return self.fault_voltages_sltg, self.I_sltg

    def calc_fault_voltages(self, Vf, Z0, Z1, Z2, I0, I1, I2):
        # Assemble impedance and current vectors
        Z_diag = np.diag([Z0, Z1, Z2])
        I_seq = np.array([I0, I1, I2], dtype=complex)
        # Prefault voltage vector: only positive sequence has Vf
        V_prefault = np.array([0, Vf, 0], dtype=complex)
        # Calculate sequence voltages at faulted bus
        Vk = V_prefault - Z_diag @ I_seq
        # returns in 0 pos neg
        return Vk

    def sequence_to_phase(self, sequence):
        # Define the operator a = exp(j*2*pi/3)
        a = np.exp(1j * 2 * np.pi / 3)
        a2 = a ** 2
        # Transformation matrix (no 1/3 scaling in this convention)
        A = np.array([
            [1, 1, 1],
            [1, a2, a],
            [1, a, a2]
        ], dtype=complex)
        seq_array = np.array(sequence, dtype=complex)
        phases = A @ seq_array
        return phases

    def calc_line_to_line(self, fault_bus: str, Zf=0):
        fault_loc = self.circuit.buses[fault_bus].index - 1  # zero-based index
        I_neg_2 = 1 / (self.Z_bus_positive[fault_loc][fault_loc] + self.Z_bus_negative[fault_loc][fault_loc] + Zf)
        I_pos_1 = -I_neg_2
        I_zero_0 = 0
        Ip: np.array = [I_zero_0, I_pos_1, I_neg_2]
        Ik = self.sequence_to_phase(Ip)
        print("Phase A Current:", np.real(Ik[0]), np.angle(Ik[0]) * 180 / np.pi)
        print("Phase B Current:", np.real(Ik[1]), np.angle(Ik[1]) * 180 / np.pi)
        print("Phase C Current:", np.real(Ik[2]), np.angle(Ik[2]) * 180 / np.pi)
        # Get sequence voltages at the faulted bus
        for bus in self.circuit.buses:
            Z0 = self.Z_bus_zero[self.circuit.buses[bus].index - 1, fault_loc]
            Z1 = self.Z_bus_positive[self.circuit.buses[bus].index - 1, fault_loc]
            Z2 = self.Z_bus_negative[self.circuit.buses[bus].index - 1, fault_loc]
            # returns in zero,pos,neg
            Vk = self.calc_fault_voltages(Vf=1, Z0=Z0, Z1=Z1, Z2=Z2, I0=I_zero_0, I1=I_pos_1, I2=I_neg_2)
            # Convert sequence voltages to phase voltages
            Vabc = self.sequence_to_phase(Vk)
            for i, phase in enumerate(['A', 'B', 'C']):
                print(f"{bus} Phase {phase}: |V| = {np.abs(Vabc[i]):.4f} p.u., ∠ = {np.angle(Vabc[i], deg=True):.2f}°")

    def calc_double_line_to_ground(self, fault_bus: str, Zf=0):
        fault_loc = self.circuit.buses[fault_bus].index - 1  # zero-based index
        num1 = self.Z_bus_negative[fault_loc][fault_loc] * (self.Z_bus_zero[fault_loc][fault_loc] + 3 * Zf)
        den1 = self.Z_bus_negative[fault_loc][fault_loc] + self.Z_bus_zero[fault_loc][fault_loc] + 3 * Zf
        num2 = self.Z_bus_zero[fault_loc][fault_loc] + 3 * Zf
        den2 = self.Z_bus_zero[fault_loc][fault_loc] + 3 * Zf + self.Z_bus_negative[fault_loc][fault_loc]
        I_pos_1 = 1 / (self.Z_bus_positive[fault_loc][fault_loc] + (num1 / den1))
        I_neg_2 = -I_pos_1 * (num2 / den2)
        I_zero_0 = -I_pos_1 * (self.Z_bus_negative[fault_loc][fault_loc] / den2)
        Ip: np.array = [I_zero_0, I_pos_1, I_neg_2]
        Ik = self.sequence_to_phase(Ip)
        print("Phase A Current:", np.real(Ik[0]), np.angle(Ik[0]) * 180 / np.pi)
        print("Phase B Current:", np.real(Ik[1]), np.angle(Ik[1]) * 180 / np.pi)
        print("Phase C Current:", np.real(Ik[2]), np.angle(Ik[2]) * 180 / np.pi)
        # Get sequence voltages at the faulted bus
        for bus in self.circuit.buses:
            Z0 = self.Z_bus_zero[self.circuit.buses[bus].index - 1, fault_loc]
            Z1 = self.Z_bus_positive[self.circuit.buses[bus].index - 1, fault_loc]
            Z2 = self.Z_bus_negative[self.circuit.buses[bus].index - 1, fault_loc]
            # returns in zero,pos,neg
            Vk = self.calc_fault_voltages(Vf=1, Z0=Z0, Z1=Z1, Z2=Z2, I0=I_zero_0, I1=I_pos_1, I2=I_neg_2)
            # Convert sequence voltages to phase voltages
            Vabc = self.sequence_to_phase(Vk)
            for i, phase in enumerate(['A', 'B', 'C']):
                print(f"{bus} Phase {phase}: |V| = {np.abs(Vabc[i]):.4f} p.u., ∠ = {np.angle(Vabc[i], deg=True):.2f}°")





