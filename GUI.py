import tkinter as tk
from Settings import Settings
from Circuit import Circuit
from Bus import Bus
from Load import Load
from Generator import Generator
from Transformer import Transformer
from Conductor import Conductor
from Geometry import Geometry
from Bundle import Bundle
from TransmissionLine import TransmissionLine
from Solution import Solution



#functions to incorporate user inputs into backend code

#add in power base and frequency
def initialize_system():
    global settings, system
    try:
        name = system_name.get().strip()
        f = float(system_frequency.get())
        s_base = float(power_base.get())
    except ValueError:
        log("⚠️ Enter valid numbers for frequency and power base.")
        return

    settings = Settings(f=f, s_base=s_base)
    system = Circuit(name, settings)
    log(f"✅ System '{name}' initialized at {f} Hz, {s_base} MVA")

#keep track of components within circuit added
def log_section(title):
    log("\n" + "=" * 40)
    log(f" {title}")
    log("=" * 40 + "\n")

def add_bus():
    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return
    try:
        name = bus_name.get().strip()
        kv = float(base_kv.get())
        type_map = {0: "pq", 1: "pv", 2: "slack"}
        btype = type_map.get(bustypebuttons.get(), "pq")
    except ValueError:
        log("⚠️ Invalid base kV.")
        return

    if name in system.buses:
        log(f"⚠️ Bus '{name}' already exists.")
        return

    # --- Slack bus check ---
    if btype == "slack":
        existing_slack = any(bus.bus_type == "slack" for bus in system.buses.values())
        if existing_slack:
            log("⚠️ Only one slack bus is allowed.")
            return

    bus = Bus(name, kv, btype)
    system.add_bus(bus)
    components_log.append(f"Bus: {name} ({kv} kV, {btype})")
    log(f"✅ Added bus '{name}' - {kv} kV - type: {btype}")

def add_transformer():
    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = xfmr_name.get().strip()
        bus1_name = xfmrbus1entry.get().strip()
        bus2_name = xfmrbus2entry.get().strip()
        z_percent = float(imp_perc.get())
        x_r_ratio = float(x_over_r.get())
        grounding_x = float(ground_x_xfmr.get())
        power_rating = float(power_rating_entry.get())

        connection_types = {0: "y-y", 1: "y-delta", 2: "delta-delta", 3: "delta-y"}
        connection_type = connection_types.get(xfmrconbut.get(), "y-y")

        if bus1_name not in system.buses or bus2_name not in system.buses:
            log("⚠️ One or both transformer buses do not exist.")
            return

        bus1 = system.buses[bus1_name]
        bus2 = system.buses[bus2_name]
    except ValueError:
        log("⚠️ Invalid transformer input (non-numeric fields).")
        return

    xfmr = Transformer(name, bus1, bus2, power_rating=power_rating,
                       impedance_percent=z_percent,
                       x_over_r_ratio=x_r_ratio,
                       connection_type=connection_type,
                       grounding_x=grounding_x)

    system.add_transformer(xfmr)
    components_log.append(f"XFMR: {name} ({bus1_name} ↔ {bus2_name}, {connection_type})")
    log(f"✅ Added Transformer '{name}' between {bus1_name} and {bus2_name}")


def add_conductor():
    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = cond_name.get().strip()
        diameter = float(condDiam.get())
        gmr_val = float(gmr.get())
        resistance = float(cond_resis.get())
        current_rating = float(cond_amp.get())
    except ValueError:
        log("⚠️ Invalid conductor input (non-numeric field).")
        return

    if name in system.conductors:
        log(f"⚠️ Conductor '{name}' already exists.")
        return

    conductor = Conductor(name, diameter, gmr_val, resistance, current_rating)
    system.add_conductor(conductor)

    components_log.append(f"Conductor: {name}")
    log(f"✅ Added Conductor '{name}' (D={diameter} in, GMR={gmr_val}, R={resistance}, I={current_rating})")


def add_geometry():
    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = geom_name.get().strip()
        xa = float(xa_entry.get())
        ya = float(ya_entry.get())
        xb = float(xb_entry.get())
        yb = float(yb_entry.get())
        xc = float(xc_entry.get())
        yc = float(yc_entry.get())
    except ValueError:
        log("⚠️ Invalid geometry coordinates (must be numeric).")
        return

    if name in system.geometries:
        log(f"⚠️ Geometry '{name}' already exists.")
        return

    geometry = Geometry(name, xa, ya, xb, yb, xc, yc)
    system.add_geometry(geometry)

    components_log.append(f"Geometry: {name}")
    log(f"✅ Added Geometry '{name}' - [A({xa},{ya}), B({xb},{yb}), C({xc},{yc})]")


def add_bundle():

    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = bundle_name.get().strip()
        spacing = float(bund_space_entry.get())
        raw_input = numcond_entry.get().strip()

        num_cond = int(raw_input)

        if num_cond < 1:
            log("⚠️ Number of conductors must be ≥ 1.")
            return
    except ValueError:
        log("⚠️ Number of conductors must be a whole number (e.g., 1, 2, 3).")
        return

    try:
        cond_name = bundle_conductor_name.get().strip()
        if cond_name not in system.conductors:
            log(f"⚠️ Conductor '{cond_name}' not found. Add it first.")
            return

        if name in system.bundles:
            log(f"⚠️ Bundle '{name}' already exists.")
            return

        conductor = system.conductors[cond_name]
        bundle = Bundle(name, int(num_cond),spacing, conductor)

        system.add_bundle(bundle)
        components_log.append(f"Bundle: {name} ({num_cond} x '{cond_name}', spacing={spacing})")
        log(f"✅ Added Bundle '{name}' using conductor '{cond_name}'")

    except Exception as e:
        log(f"❌ Error in add_bundle: {e}")




def add_transmission_line():
    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = tline_name_entry.get().strip()
        bus1_name = tline_bus1_entry.get().strip()
        bus2_name = tline_bus2_entry.get().strip()
        length = float(tline_length_entry.get())
    except ValueError:
        log("⚠️ Invalid line length.")
        return

    if name in system.transmission_lines:
        log(f"⚠️ Transmission line '{name}' already exists.")
        return
    if bus1_name not in system.buses or bus2_name not in system.buses:
        log("⚠️ One or both bus names do not exist.")
        return
    if not hasattr(system, 'bundles') or not system.bundles:
        log("⚠️ No bundles defined. Add a bundle first.")
        return
    if not system.geometries:
        log("⚠️ No geometries defined. Add a geometry first.")
        return

    # Use the most recently added bundle and geometry
    bundle_name = list(system.bundles)[-1]
    geometry_name = list(system.geometries)[-1]

    bundle = system.bundles[bundle_name]
    geometry = system.geometries[geometry_name]
    bus1 = system.buses[bus1_name]
    bus2 = system.buses[bus2_name]

    tline = TransmissionLine(name, bus1, bus2, bundle, geometry, length)
    system.add_transmission_line(tline)

    components_log.append(f"T-Line: {name} ({bus1_name} → {bus2_name}, {length} mi)")
    log(f"✅ Added Transmission Line '{name}' using bundle '{bundle_name}' and geometry '{geometry_name}'")



def add_load():
    global system, settings
    if system is None or settings is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = load_name_entry.get().strip()
        bus_name = load_bus_entry.get().strip()
        p = float(p_load_entry.get())
        q = float(q_load_entry.get())
    except ValueError:
        log("⚠️ Invalid real or reactive power (P/Q).")
        return

    if bus_name not in system.buses:
        log(f"⚠️ Bus '{bus_name}' does not exist.")
        return
    if name in system.loads:
        log(f"⚠️ Load '{name}' already exists.")
        return

    bus = system.buses[bus_name]
    load = Load(name, bus, p, q, settings)
    system.add_load(load)

    components_log.append(f"Load: {name} ({p} + j{q} MVA) at {bus_name}")
    log(f"✅ Added Load '{name}' with P={p} MW, Q={q} MVar on Bus '{bus_name}'")

def add_generator():
    global system, settings
    if system is None or settings is None:
        log("⚠️ Initialize system first.")
        return

    try:
        name = gen_name_entry.get().strip()
        bus_name = gen_bus_entry.get().strip()
        V_set = float(gen_voltage_entry.get())
        x1 = float(gen_x1_entry.get())
        x2 = float(gen_x2_entry.get())
        x0 = float(gen_x0_entry.get())
        grounding_x = float(gen_ground_x_entry.get())
        mw_set = float(mw_setpoint_entry.get())
    except ValueError:
        log("⚠️ Invalid generator parameters.")
        return

    if bus_name not in system.buses:
        log(f"⚠️ Bus '{bus_name}' does not exist.")
        return
    if name in system.generators:
        log(f"⚠️ Generator '{name}' already exists.")
        return

    bus = system.buses[bus_name]
    gen = Generator(name, bus, voltage_setpoint=V_set, mw_setpoint=mw_set,
                    x1=x1, x2=x2, x0=x0, grounding_x=grounding_x,
                    grounded=True, settings=settings)

    system.add_generator(gen)
    components_log.append(f"Generator: {name} at {bus_name} (Vset={V_set}, X1={x1})")
    log(f"✅ Added Generator '{name}' on Bus '{bus_name}' with Vset={V_set}, X1={x1}, X2={x2}, X0={x0}")


def run_power_flow():
    global system
    if system is None:
        log("⚠️ Initialize system first.")
        return

    try:
        log(" Running Power Flow...")
        log(f" Circuit Summary: {len(system.buses)} buses, {len(system.loads)} loads, {len(system.generators)} gens")

        # Debug list of buses
        log(" Buses:")
        for name, bus in system.buses.items():
            log(f"• {name}: {bus.base_kv} kV, type={bus.bus_type}, V={bus.v_pu:.4f}, Δ={bus.delta:.2f}°")

        # Debug list of loads
        log(" Loads:")
        for name, load in system.loads.items():
            log(f"• {name} at {load.bus.name}: P={load.real_pwr:.2f} MW, Q={load.reactive_pwr:.2f} MVar")

        # Debug list of generators
        log(" Generators:")
        for name, gen in system.generators.items():
            log(f"• {name} at {gen.bus.name}: Vset={gen.voltage_setpoint}, MW={gen.mw_setpoint}")

        log(" Transmission Lines:")
        for name, line in system.transmission_lines.items():
            assert isinstance(line.bundle, Bundle), f"❌ Bundle for line '{name}' is not a valid Bundle object!"
            assert isinstance(line.geometry, Geometry), f"❌ Geometry for line '{name}' is not a valid Geometry object!"

            log(f"• {name}: {line.bus1.name} ↔ {line.bus2.name}, Length={line.length} mi")
            log(f"   ↪ Bundle: {line.bundle.name} ({line.bundle.num_conductors} × {line.bundle.conductor.name}, spacing={line.bundle.spacing})")
            log(f"   ↪ Geometry: {line.geometry.name} (xa={line.geometry.xa}, xb={line.geometry.xb}, xc={line.geometry.xc})")

        solver = Solution(system)
        log_section("Bus Information")
        for name, bus in system.buses.items():
            log(f"• {name}: {bus.base_kv} kV, type={bus.bus_type}, V={bus.v_pu:.4f}, ∠ = {bus.delta:.2f}°")

        log(" Transformer Y-Prim Matrices:")
        for name, xfmr in system.transformers.items():
            log(f"\n{name} Y Prim: Positive Sequence")
            log(xfmr.y_prim_positive.to_string())

        log("\n Transmission Line Y-Prim Matrices:")
        for name, line in system.transmission_lines.items():
            log(f"\n{name} Y Prim: Positive Sequence")
            log(line.y_prim.to_string())
        log(" All Bus Names in System:")
        for bname in system.buses.keys():
            log(f"• '{bname}'")


        log(" Calculating Y-bus...")
        system.calc_y_bus()

        log(" Computing known powers...")
        solver.calc_known_power()

        log(" Calculating mismatch vector...")
        solver.calc_mismatch()

        log(" Forming Jacobian...")
        solver.calc_jacobian()

        log(" Setting initial guess (flat or non-flat)...")
        solver.calc_solutionRef()

        log(" Starting Newton-Raphson iterations...")
        converged_values, iterations = solver.calc_solution()

        if converged_values is not None:
            log(f"✅ Power flow converged in {iterations} iterations.")
            log(" Final Bus Voltages:")
            for i, (v, a) in enumerate(converged_values):
                log(f"• Bus {i + 1}: |V| = {v:.4f} pu, ∠ = {a:.2f}°")
        else:
            log("⚠️ Power flow did not converge within max iterations.")

    except Exception as e:
        log(f"❌ Power flow failed: {e}")




components_log = []
maingui = tk.Tk()
maingui.config(bg="#a79f9f")
maingui.title("Power Simulator")
maingui.geometry("1500x1500")

#following code is all format and visual setup of GUI

#**********SYSTEM SETUP**********************************
systemLabel = tk.Label(master=maingui, text="General System Setup")
systemLabel.config(bg="#f1a5a5", fg="#000", font=("", 10, ))
systemLabel.place(x=0, y=0, width=240, height=40)

systemNamelabel = tk.Label(master=maingui, text="System Name")
systemNamelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
systemNamelabel.place(x=0, y=40, width=120, height=40)

system_name = tk.Entry(master=maingui)
system_name.config(bg="#fff", fg="#000", font=("", 10, ), cursor="arrow")
system_name.place(x=120, y=40, width=120, height=40)

pbaselabel = tk.Label(master=maingui, text="Power Base (MVA)")
pbaselabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
pbaselabel.place(x=0, y=80, width=120, height=40)

power_base = tk.Entry(master=maingui)
power_base.config(bg="#fff", fg="#000", font=("", 10, ))
power_base.place(x=120, y=80, width=120, height=40)

baseflabel = tk.Label(master=maingui, text="Base Frequency (Hz)")
baseflabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
baseflabel.place(x=0, y=120, width=120, height=40)

system_frequency = tk.Entry(master=maingui)
system_frequency.config(bg="#fff", fg="#000", font=("", 10, ), cursor="arrow")
system_frequency.place(x=120, y=120, width=120, height=40)

initsys = tk.Button(master=maingui, text="initialize")
initsys.place(x=0, y=160, width=240, height=40)


initsys.config(command=initialize_system,bg="#c3ef9f", fg="#000", font=("", 10, ))
#*******************************************************************************

#********************BUS INTERFACE**********************************************
buslabel = tk.Label(master=maingui, text="Buses")
buslabel.config(bg="#f7aaaa", fg="#000", font=("", 10, ))
buslabel.place(x=0, y=200, width=240, height=40)

busnamelabel = tk.Label(master=maingui, text="Name")
busnamelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
busnamelabel.place(x=0, y=240, width=120, height=40)

bus_name = tk.Entry(master=maingui)
bus_name.config(bg="#fff", fg="#000", font=("", 10, ))
bus_name.place(x=120, y=240, width=120, height=40)

basekvlabel = tk.Label(master=maingui, text="base kV")
basekvlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
basekvlabel.place(x=0, y=280, width=120, height=40)

base_kv = tk.Entry(master=maingui)
base_kv.config(bg="#fff", fg="#000", font=("", 10, ))
base_kv.place(x=120, y=280, width=120, height=40)

bustypelabel = tk.Label(master=maingui, text="Type")
bustypelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
bustypelabel.place(x=0, y=320, width=120, height=40)

bustypebuttons = tk.IntVar()

bustypebuttons_0 = tk.Radiobutton(master=maingui, variable=bustypebuttons, text="PQ")
bustypebuttons_0.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=0)
bustypebuttons_0.place(x=120, y=320)

bustypebuttons_1 = tk.Radiobutton(master=maingui, variable=bustypebuttons, text="PV")
bustypebuttons_1.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=1)
bustypebuttons_1.place(x=120, y=340)

bustypebuttons_2 = tk.Radiobutton(master=maingui, variable=bustypebuttons, text="Slack")
bustypebuttons_2.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=2)
bustypebuttons_2.place(x=162, y=330)

busButton = tk.Button(master=maingui, text="Add bus")

busButton.place(x=0, y=360, width=240, height=40)


busButton.config(command=add_bus,bg="#c1e7a1", fg="#000", font=("", 10, ))
#************************************************************

#***************TRANSFORMER INTERFACE*************************
XFMRlabel = tk.Label(master=maingui, text="Transformers")
XFMRlabel.config(bg="#eda7a7", fg="#000", font=("", 10, ))
XFMRlabel.place(x=0, y=400, width=240, height=40)

xfmrName = tk.Label(master=maingui, text="Name")
xfmrName.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
xfmrName.place(x=0, y=440, width=120, height=40)

xfmr_name = tk.Entry(master=maingui)
xfmr_name.config(bg="#fff", fg="#000", font=("", 10, ))
xfmr_name.place(x=120, y=440, width=120, height=40)

conLabel = tk.Label(master=maingui, text="Connection buses")
conLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
conLabel.place(x=0, y=480, width=240, height=40)

bus1label = tk.Label(master=maingui, text="Bus 1")
bus1label.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
bus1label.place(x=0, y=520, width=120, height=40)

xfmrbus1entry = tk.Entry(master=maingui)
xfmrbus1entry.config(bg="#fff", fg="#000", font=("", 10, ))
xfmrbus1entry.place(x=120, y=520, width=120, height=40)

bus2label = tk.Label(master=maingui, text="Bus 2")
bus2label.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
bus2label.place(x=0, y=560, width=120, height=40)

xfmrbus2entry = tk.Entry(master=maingui)
xfmrbus2entry.config(bg="#fff", fg="#000", font=("", 10, ))
xfmrbus2entry.place(x=120, y=560, width=120, height=40)

impedpercentlabel = tk.Label(master=maingui, text="Impedance percent")
impedpercentlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
impedpercentlabel.place(x=0, y=600, width=120, height=40)

imp_perc = tk.Entry(master=maingui)
imp_perc.config(bg="#fff", fg="#000", font=("", 10, ))
imp_perc.place(x=120, y=600, width=120, height=40)

xrlabel = tk.Label(master=maingui, text="X/R ratio")
xrlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
xrlabel.place(x=0, y=640, width=120, height=40)

x_over_r = tk.Entry(master=maingui)
x_over_r.config(bg="#fff", fg="#000", font=("", 10, ))
x_over_r.place(x=120, y=640, width=120, height=40)

connectypelabel = tk.Label(master=maingui, text="Connection type")
connectypelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
connectypelabel.place(x=0, y=680, width=240, height=40)

xfmrconbut = tk.IntVar()
xfmrconbut_0 = tk.Radiobutton(master=maingui, variable=xfmrconbut, text="y-y")
xfmrconbut_0.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=0)
xfmrconbut_0.place(x=0, y=720)
xfmrconbut_1 = tk.Radiobutton(master=maingui, variable=xfmrconbut, text="y-delta")
xfmrconbut_1.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=1)
xfmrconbut_1.place(x=42, y=720)
xfmrconbut_2 = tk.Radiobutton(master=maingui, variable=xfmrconbut, text="delta-delta")
xfmrconbut_2.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=2)
xfmrconbut_2.place(x=101, y=720)
xfmrconbut_3 = tk.Radiobutton(master=maingui, variable=xfmrconbut, text="delta-y")
xfmrconbut_3.config(bg="#E4E2E2", fg="#000", font=("", 10, ), value=3)
xfmrconbut_3.place(x=177, y=720)

groundxlabel = tk.Label(master=maingui, text="Grounding impedance")
groundxlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
groundxlabel.place(x=0, y=760, width=120, height=40)

ground_x_xfmr = tk.Entry(master=maingui)
ground_x_xfmr.config(bg="#fff", fg="#000", font=("", 10, ))
ground_x_xfmr.place(x=120, y=760, width=120, height=40)

power_ratinglabel = tk.Label(master=maingui, text="Power Rating")
power_ratinglabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
power_ratinglabel.place(x=0, y=800, width=120, height=40)

power_rating_entry = tk.Entry(master=maingui)
power_rating_entry.config(bg="#fff", fg="#000", font=("", 10, ))
power_rating_entry.place(x=120, y=800, width=120, height=40)



add_xfmr = tk.Button(master=maingui, text="Add XFMR")

add_xfmr.place(x=0, y=840, width=240, height=40)


add_xfmr.config(command=add_transformer, bg="#d2f1b6", fg="#000", font=("", 10,))
#**************************************************************************
#************CONDUCTOR INTERFACE*****************************************

conductorLabel = tk.Label(master=maingui, text="Conductor")
conductorLabel.config(bg="#eca9a9", fg="#000", font=("", 10, ))
conductorLabel.place(x=240, y=0, width=240, height=40)

condName = tk.Label(master=maingui, text="Name")
condName.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
condName.place(x=240, y=40, width=120, height=40)

cond_name = tk.Entry(master=maingui)
cond_name.config(bg="#fff", fg="#000", font=("", 10, ))
cond_name.place(x=360, y=40, width = 120,height=40)

diamLabel = tk.Label(master=maingui, text="Diameter")
diamLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
diamLabel.place(x=240, y=80,width = 120, height=40)

condDiam = tk.Entry(master=maingui)
condDiam.config(bg="#fff", fg="#000", font=("", 10, ))
condDiam.place(x=360, y=80,width = 120, height=40)

gmrLabel = tk.Label(master=maingui, text="GMR")
gmrLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
gmrLabel.place(x=240, y=120, width = 120,height=40)

gmr = tk.Entry(master=maingui)
gmr.config(bg="#fff", fg="#000", font=("", 10, ))
gmr.place(x=360, y=120,width = 120, height=40)

resLabel = tk.Label(master=maingui, text="Resistance")
resLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
resLabel.place(x=240, y=160,width = 120, height=40)

cond_resis = tk.Entry(master=maingui)
cond_resis.config(bg="#fff", fg="#000", font=("", 10, ))
cond_resis.place(x=360, y=160, width = 120,height=40)

ampLabel = tk.Label(master=maingui, text="Amperage")
ampLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
ampLabel.place(x=240, y=200, width=120, height=40)

cond_amp = tk.Entry(master=maingui)
cond_amp.config(bg="#fff", fg="#000", font=("", 10, ))
cond_amp.place(x=360, y=200, width=120, height=40)

add_cond = tk.Button(master=maingui, text="Add Conductor")
add_cond.config(command=add_conductor, bg="#cff1af", fg="#000", font=("", 10,))
add_cond.place(x=240, y=240, width = 240,height=40)
#*****************************************************************
#**************GEOMETRY INTERFACE*********************************
geomLabel = tk.Label(master=maingui, text="Geometry")
geomLabel.config(bg="#ecaeae", fg="#000", font=("", 10, ))
geomLabel.place(x=240, y=280, width=240, height=40)

geomName = tk.Label(master=maingui, text="Name")
geomName.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
geomName.place(x=240, y=320, width=120, height=40)

geom_name = tk.Entry(master=maingui)
geom_name.config(bg="#fff", fg="#000", font=("", 10, ))
geom_name.place(x=360, y=320, width = 120,height=40)

xaLabel = tk.Label(master=maingui, text="Xa")
xaLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
xaLabel.place(x=240, y=360, width=120, height=40)

xa_entry = tk.Entry(master=maingui)
xa_entry.config(bg="#fff", fg="#000", font=("", 10, ))
xa_entry.place(x=360, y=360,width = 120, height=40)

yaLabel = tk.Label(master=maingui, text="Ya")
yaLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
yaLabel.place(x=240, y=400, width=120, height=40)

ya_entry = tk.Entry(master=maingui)
ya_entry.config(bg="#fff", fg="#000", font=("", 10, ))
ya_entry.place(x=360, y=400, width=120, height=40)

xbLabel = tk.Label(master=maingui, text="Xb")
xbLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
xbLabel.place(x=240, y=440, width=120, height=40)

xb_entry = tk.Entry(master=maingui)
xb_entry.config(bg="#fff", fg="#000", font=("", 10, ))
xb_entry.place(x=360, y=440, width=120, height=40)

ybLabel = tk.Label(master=maingui, text="Yb")
ybLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
ybLabel.place(x=240, y=480, width=120, height=40)

yb_entry = tk.Entry(master=maingui)
yb_entry.config(bg="#fff", fg="#000", font=("", 10, ))
yb_entry.place(x=360, y=480, width=120, height=40)

xcLabel = tk.Label(master=maingui, text="Xc")
xcLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
xcLabel.place(x=240, y=520, width=120, height=40)

xc_entry = tk.Entry(master=maingui)
xc_entry.config(bg="#fff", fg="#000", font=("", 10, ))
xc_entry.place(x=360, y=520, width=120, height=40)

ycLabel = tk.Label(master=maingui, text="Yc")
ycLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
ycLabel.place(x=240, y=560, width=120, height=40)

yc_entry = tk.Entry(master=maingui)
yc_entry.config(bg="#fff", fg="#000", font=("", 10, ))
yc_entry.place(x=360, y=560, width=120, height=40)

geomBut = tk.Button(master=maingui, text="Add Geometry")
geomBut.config(command=add_geometry, bg="#c4e4ae", fg="#000", font=("", 10,))
geomBut.place(x=240, y=600,width = 240, height=40)
#****************************************************************

#*****************BUNDLE INTERFACE***********************
bundLabel = tk.Label(master=maingui, text="Bundle")
bundLabel.config(bg="#f9bdbd", fg="#000", font=("", 10, ))
bundLabel.place(x=240, y=640, width=240, height=40)

bundNamelabel = tk.Label(master=maingui, text="Name")
bundNamelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
bundNamelabel.place(x=240, y=680, width=120, height=40)

bundle_name = tk.Entry(master=maingui)
bundle_name.config(bg="#fff", fg="#000", font=("", 10, ))
bundle_name.place(x=360, y=680, width=120, height=40)

bundspaclabel = tk.Label(master=maingui, text="Spacing")
bundspaclabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
bundspaclabel.place(x=240, y=720, width=120, height=40)

bund_space_entry = tk.Entry(master=maingui)
bund_space_entry.config(bg="#fff", fg="#000", font=("", 10, ))
bund_space_entry.place(x=360, y=720, width=120, height=40)

numCondLabel = tk.Label(master=maingui, text="Number of Conductors")
numCondLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
numCondLabel.place(x=240, y=760, width=120, height=40)

numcond_entry = tk.Entry(master=maingui)
numcond_entry.config(bg="#fff", fg="#000", font=("", 10, ))
numcond_entry.place(x=360, y=760, width=120, height=40)

bundconductorlabel = tk.Label(master=maingui, text="Conductor Name")
bundconductorlabel.config(bg="#E4E2E2", fg="#000", font=("", 10,))
bundconductorlabel.place(x=240, y=800 , width=120, height=40)

bundle_conductor_name = tk.Entry(master=maingui)
bundle_conductor_name.config(bg="#fff", fg="#000", font=("", 10,))
bundle_conductor_name.place(x=360, y=800 , width=120, height=40)



bundbut = tk.Button(master=maingui, text="Add Bundle")
bundbut.config(command=add_bundle, bg="#d8f1c1", fg="#000", font=("", 10,))

bundbut.place(x=240, y=840, width=240, height=40)
#**********************************************************************
#*****************TRANSMISSION LINE INTERFACE***************************
tlineLabel = tk.Label(master=maingui, text="Transmission Line")
tlineLabel.config(bg="#fababa", fg="#000", font=("", 10, ))
tlineLabel.place(x=480, y=0, width = 240,height=40)

tlineNamelabel = tk.Label(master=maingui, text="Name")
tlineNamelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
tlineNamelabel.place(x=480, y=40, width=120, height=40)

tline_name_entry = tk.Entry(master=maingui)
tline_name_entry.config(bg="#fff", fg="#000", font=("", 10, ))
tline_name_entry.place(x=600, y=40, width=120, height=40)

startbusLabel = tk.Label(master=maingui, text="Starting bus")
startbusLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
startbusLabel.place(x=480, y=80, width=120, height=40)

tline_bus1_entry = tk.Entry(master=maingui)
tline_bus1_entry.config(bg="#fff", fg="#000", font=("", 10, ))
tline_bus1_entry.place(x=600, y=80, width=120, height=40)

endbusLabel = tk.Label(master=maingui, text="Ending bus")
endbusLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
endbusLabel.place(x=480, y=120, width=120, height=40)

tline_bus2_entry = tk.Entry(master=maingui)
tline_bus2_entry.config(bg="#fff", fg="#000", font=("", 10, ))
tline_bus2_entry.place(x=600, y=120, width=120, height=40)

tlinelengthlabel = tk.Label(master=maingui, text="Length")
tlinelengthlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
tlinelengthlabel.place(x=480, y=160, width=120, height=40)

tline_length_entry = tk.Entry(master=maingui)
tline_length_entry.config(bg="#fff", fg="#000", font=("", 10, ))
tline_length_entry.place(x=600, y=160, width=120, height=40)

tlinebut = tk.Button(master=maingui, text="Add Tline")
tlinebut.config(command=add_transmission_line,bg="#d8ecbb", fg="#000", font=("", 10, ))
tlinebut.place(x=480, y=200, width=240, height=40)
#*************************************************************
#*****************LOAD INTERFACE****************************

loadlabel = tk.Label(master=maingui, text="Load")
loadlabel.config(bg="#f7bcbc", fg="#000", font=("", 10, ))
loadlabel.place(x=480, y=240, width=240, height=40)


loadnamelabel = tk.Label(master=maingui, text="Name")
loadnamelabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
loadnamelabel.place(x=480, y=280, width=120, height=40)

load_name_entry = tk.Entry(master=maingui)
load_name_entry.config(bg="#fff", fg="#000", font=("", 10, ))
load_name_entry.place(x=600, y=280, width=120, height=40)

loadBusLabel = tk.Label(master=maingui, text="Bus")
loadBusLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
loadBusLabel.place(x=480, y=320, width=120, height=40)

load_bus_entry = tk.Entry(master=maingui)
load_bus_entry.config(bg="#fff", fg="#000", font=("", 10, ))
load_bus_entry.place(x=600, y=320, width=120, height=40)

pLabelload = tk.Label(master=maingui, text="P")
pLabelload.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
pLabelload.place(x=480, y=360, width=120, height=40)

p_load_entry = tk.Entry(master=maingui)
p_load_entry.config(bg="#fff", fg="#000", font=("", 10, ))
p_load_entry.place(x=600, y=360, width=120, height=40)

qlabelload = tk.Label(master=maingui, text="Q")
qlabelload.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
qlabelload.place(x=480, y=400, width=120, height=40)

q_load_entry = tk.Entry(master=maingui)
q_load_entry.config(bg="#fff", fg="#000", font=("", 10, ))
q_load_entry.place(x=600, y=400, width=120, height=40)

loadbut = tk.Button(master=maingui, text="Add load")
loadbut.config(command=add_load, bg="#e1f5c4", fg="#000", font=("", 10,))

loadbut.place(x=480, y=440, width=240, height=40)
#**************************************************************
#************************GENERATOR INTERFACE*******************

genLabel = tk.Label(master=maingui, text="Generator")
genLabel.config(bg="#f2b4b4", fg="#000", font=("", 10, ))
genLabel.place(x=480, y=480,width =240, height=40)

genNameLabel = tk.Label(master=maingui, text="Name")
genNameLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genNameLabel.place(x=480, y=520, width=120, height=40)

gen_name_entry = tk.Entry(master=maingui)
gen_name_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_name_entry.place(x=600, y=520, width=120, height=40)

genBusLabel = tk.Label(master=maingui, text="bus")
genBusLabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genBusLabel.place(x=480, y=560, width=120, height=40)

gen_bus_entry = tk.Entry(master=maingui)
gen_bus_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_bus_entry.place(x=600, y=560, width=120, height=40)

genvollabel = tk.Label(master=maingui, text="set Voltage")
genvollabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genvollabel.place(x=480, y=600, width=120, height=40)

gen_voltage_entry = tk.Entry(master=maingui)
gen_voltage_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_voltage_entry.place(x=600, y=600, width=120, height=40)

genx1Label = tk.Label(master=maingui, text="X1")
genx1Label.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genx1Label.place(x=480, y=640, width=120, height=40)

gen_x1_entry = tk.Entry(master=maingui)
gen_x1_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_x1_entry.place(x=600, y=640, width=120, height=40)

genx2Label = tk.Label(master=maingui, text="X2")
genx2Label.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genx2Label.place(x=480, y=680, width=120, height=40)

gen_x2_entry = tk.Entry(master=maingui)
gen_x2_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_x2_entry.place(x=600, y=680, width=120, height=40)

genx0label = tk.Label(master=maingui, text="X0")
genx0label.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genx0label.place(x=480, y=720, width=120, height=40)

gen_x0_entry = tk.Entry(master=maingui)
gen_x0_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_x0_entry.place(x=600, y=720, width=120, height=40)

genGroundXlabel = tk.Label(master=maingui, text="Grounding X")
genGroundXlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
genGroundXlabel.place(x=480, y=760, width=120, height=40)

gen_ground_x_entry = tk.Entry(master=maingui)
gen_ground_x_entry.config(bg="#fff", fg="#000", font=("", 10, ))
gen_ground_x_entry.place(x=600, y=760, width=120, height=40)

mwsetpointlabel = tk.Label(master=maingui, text="MW Setpoint")
mwsetpointlabel.config(bg="#E4E2E2", fg="#000", font=("", 10, ))
mwsetpointlabel.place(x=480, y=800, width=120, height=40)

mw_setpoint_entry = tk.Entry(master=maingui)
mw_setpoint_entry.config(bg="#fff", fg="#000", font=("", 10, ))
mw_setpoint_entry.place(x=600, y=800, width=120, height=40)

genbut = tk.Button(master=maingui, text="Add Generator")
genbut.config(command=add_generator, bg="#c6f4b6", fg="#000", font=("", 10,))

genbut.place(x=480, y=840, width = 240,height=40)

output_box = tk.Text(master=maingui, bg="#fff", fg="#000", font=("", 10, ))
output_box.place(x=840, y=100, width=500, height=500)

def run_power_flow_callback(event=None):
    run_power_flow()

# Create canvas and green background rectangle
button_canvas = tk.Canvas(master=maingui, width=300, height=90, bg="#a79f9f", highlightthickness=0)
button_canvas.place(x=950, y=670)

# Draw green rounded rectangle
button_canvas.create_rectangle(0, 0, 300, 90, fill="#98FB98", outline="#32CD32", width=2)

# Add centered text
button_canvas.create_text(150, 45, text="Run Power Flow", font=("", 14, "bold"), fill="black")

# Bind click event to the canvas
button_canvas.bind("<Button-1>", run_power_flow_callback)


def log(msg):
    output_box.insert(tk.END, f"{msg}\n")
    output_box.see(tk.END)
maingui.mainloop()