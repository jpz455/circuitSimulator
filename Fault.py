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
    self.Ifn = fault_v / Znn

    # Faulted bus voltages
    self.fault_voltages = np.empty(len(self.circuit.buses), dtype=np.complex128)
    for k, bus in enumerate(self.circuit.buses.values()):
        self.fault_voltages[k] = (1 - self.z_bus[k][index] / Znn) * fault_v

    return self.fault_voltages, self.Ifn

def print_fault_voltages(self):
    print("Fault Current Magnitude: ", round(np.real(self.Ifn), 5))
    for i, v in enumerate(self.fault_voltages):
        print("Bus", i + 1, " voltage magnitude:", round(np.real(v), 5))


def calc_single_line_to_ground(self, fault_bus: str, Zf=0, fault_v = 1.0):


    # Get Znn at faulted bus
    index = self.circuit.buses[fault_bus].index - 1
    Znn = self.z_bus[index][index]

    # connect all sequences in series


    return None

def calc_line_to_line(self, fault_bus: str, Zf=0):


    return None

def calc_double_line_to_ground(self, fault_bus: str, Zf=0):


    return None









