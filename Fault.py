from Circuit import Circuit
import numpy as np
import pandas as pd

class Fault:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

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
        self.circuit.calc_y_bus()
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

    def calc_faulted_zbus(self, fault_type: str, fault_bus: str, fault_v=1.0):
        """
        Calculates the faulted Zbus matrix for different fault types (Line-to-Ground, Line-to-Line, etc.)
        """
        # Recalculate Ybus for the system, considering transformers and generators
        self.circuit.calc_y_bus()

        # Modify Ybus based on fault type
        if fault_type == "line_to_ground":
            self.ybus_faulted = self.line_to_ground_fault()
        elif fault_type == "line_to_line":
            self.ybus_faulted = self.line_to_line_fault()
        elif fault_type == "double_line_to_ground":
            self.ybus_faulted = self.double_line_to_ground_fault()
        else:
            raise ValueError("Invalid fault type. Choose from 'line_to_ground', 'line_to_line', 'double_line_to_ground'.")

        # Invert the faulted Ybus matrix to get Zbus
        self.zbus_faulted = np.linalg.inv(np.array(self.ybus_faulted))

        # Get Znn for faulted bus
        index = self.circuit.buses[fault_bus].index - 1
        Znn_faulted = self.zbus_faulted[index][index]

        # Calculate fault current
        self.Ifn_faulted = fault_v / Znn_faulted

        # Print the results
        print(f"Faulted Zbus Matrix (Inverted Ybus) for {fault_type} at bus {fault_bus}:")
        print(pd.DataFrame(self.zbus_faulted, index=self.circuit.busRef, columns=self.circuit.busRef))

        print(f"Fault Current Magnitude at {fault_bus}: ", round(np.real(self.Ifn_faulted), 5))

        return self.zbus_faulted, self.Ifn_faulted

    def line_to_ground_fault(self):
        """
        Modify Ybus for a Line-to-Ground fault, considering transformers and generators.
        """
        # Initialize Ybus for the system
        ybus = pd.DataFrame(np.zeros((len(self.circuit.buses), len(self.circuit.buses))),
                            index=self.circuit.busRef, columns=self.circuit.busRef)

        # Loop through all transmission lines
        for line in self.circuit.transmission_lines:
            # Add transmission line sequence impedances to the Ybus matrix
            ybus = self.add_line_impedance_to_ybus(ybus, str(self.circuit.transmission_lines[line].bus1))

        # Loop through all transformers
        for transformer in self.circuit.transformers:
            # Add transformer sequence impedance to the Ybus matrix
            ybus = self.add_transformer_impedance_to_ybus(ybus, transformer)

        # Loop through all generators
        for generator in self.circuit.generators:
            # Add generator sequence impedance to the Ybus matrix
            ybus = self.add_generator_impedance_to_ybus(ybus, generator)

        return ybus

    def solveLineToLineFault(self, index1, Vf, Zf):
        Zf = Zf / self.circuit.buses[index1].z_base
        V012 = np.zeros((7, 3), dtype=complex)
        faultcurrentpos = Vf / (self.circuit.zBus1[index1, index1] + self.circuit.zBus2[index1, index1] + Zf)
        faultcurrentneg = -faultcurrentpos
        faultcurrentzero = 0
        faultcurrents012 = np.matrix([faultcurrentzero, faultcurrentpos, faultcurrentneg])
        for k in range(0, 7):
            V012[k, 0] = 0 - self.circuit.zBus0[k, index1] * faultcurrentzero
            V012[k, 1] = Vf - self.circuit.zBus1[k, index1] * faultcurrentpos
            V012[k, 2] = 0 - self.circuit.zBus0[k, index1] * faultcurrentneg
        faultcurrentsabc = self.get012toabc(faultcurrents012)
        Vabc = self.get012toabc(V012)

        self.print_fault_v_i(index1,Vabc, faultcurrentsabc)








