# __Circuit Simulator Interface__

## Purpose and Scope
This software is designed to simulate power flow circuits (i.e.: three-phase power distribution systems) including generators, loads, bundled transmission lines, transformers, and loads. Users can input components and run power flow analysis to solve the system (utilizing the Newton-Raphson algorithm) or analyze fault studies (both balanced and unbalanced). This specific branch incorporates a graphical user interface (GUI) to enable more dynamic, visual user interaction.

## Input and Output
Users input circuit component information through a series of push button selection and dialog box text input (see sections Executing Test Suit and Executing Normal Use Case for further details). Output (i.e.: solution voltages, currents, fault currents, and circuit components) are displayed on GUI screens on appropriate tabs. 

## Set-Up
To use this software, users should create their development environment. Python is required; version 3.12 or 3.11 is recommended. Dependencies required include NumPy, PyQt, and Pandas.   
The IDE PyCharm is recommended, though a recommended flow of operations to run the software from a terminal follows:

1. Download and unzip the files to a preferred location in storage.
2. Open a Python terminal and navigate to the correct directory where the code files are stored.
3. Enter command python3 -m venv venvName to create a virtual environment (venv).
4. Enter command source venvName/bin/activate (for Linux) or venvName\Scripts\activate to activate the venv.
5. Enter command pip install pyqt5 numpy pandas to install required dependencies.
6. To verify packages were installed correctly, use command pip list and visually inspect for PyQt5, NumPy, and Pandas.
7. The software is ready to be executed.

## Executing Test Suite
Testing relies on visual inspection. The following steps outline the procedure:
1. To run the test circuit, open the GUI by running the command main.py. A GUI window will open. 
2. Navigate to the tab labeled "Load Test Circuit" and select the push button labeled "Load Test Circuit." Values will populate the table below.
3. Navigate to the tab labeled "Solve Power Flow" and select the push button labeled "Solve Power Flow." Values will populate the table below.
4. Compare the values with the printed output in the terminal, or compare with the values from PowerWorld in the folder "PowerWorld Files."
5. To compare fault values, navigate to the tab "Fault Study" and select the push button labeled "Fault Bus." Enter "bus5" when prompted for the fault bus name and "1" for the fault voltage. 
6. Select the desired fault to calculate; compare values with PowerWorld files.

## Executing Normal Use Case
For main GUI execution, run the command python main.py. A GUI window will open.

1. First select tab titled "Add Components." A screen will display with push buttons to add buses, lines, transformers, loads, and generators.
2. Buses must be added first. Once the button "Add Bus" is selected, a series of dialog boxes will pop up with instructions to add bus name, type, voltage base, voltage per unit value, and angle. Once a bus is added, it will appear under the heading "buses" below the buttons.
3. To add other components, simply select the button corresponding to the desired component and add the appropriate input in the dialog box following the prompts.
4. It should be noted that the first transmission line requires information regarding the conductor data, conductor geometry, and bundle spacing. Dialog boxes will instruct the user to enter such information. Once the first line is added, these data are saved for further lines.
5. Once the circuit is finished, select "Solve Power Flow" and click the large button "Solve Power Flow" to solve the system. If it can solved, the screen will populate with the solution per-unit voltages at each bus. If the circuit is unsolvable, the window will close.
6. To run a fault study, navigate to the tab labeled "Fault Study" and select the large button "Fault Bus." Dialog boxes will open with instructions to enter the fault bus's name and fault voltage. Once this information has been input, the subsequent buttons for 3 phase balanced faults, line-to-line faults, single line to ground faults, and double line to ground faults will be enabled. Click on any of these buttons to run that study; solution details will populate below.
7. To select a different fault study or run power flow, simply navigate to the desired tab and button and click. The circuit will be saved, and the new study will run and populate.

## Validation
GUI output has been verified against the existing codebase (i.e.: command-line outputs). As the calculations involved in populating the GUI are not different from those involved in command-line (Project 2) output, the code has been validation against both the existing printed values in the terminal as well as against PowerWorld's output.
See the Validation folder for screenshots of expected outputs and PowerWorld outputs.

## References
Eyre, Ian. (n.d.) How to format floats within f-strings in Python. https://realpython.com/how-to-python-f-string-format-float/
Fitpatrick, M. (2024, November 26). Creating your first app with PyQt5. https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/
Fitzpatrick, M. (2025, March 19). The complete PyQt5 tutorial- Create GUI applications with Python. PythonGUIs. https://www.pythonguis.com/pyqt5/
Geeks for Geeks. (2025, April 25). PyQt5- How to align text of label. https://www.geeksforgeeks.org/pyqt5-how-to-align-text-of-label/
Geeks for Geeks. (2020, March 26). PyQt5- How to set minimum size of window | setMinimumSize method. https://www.geeksforgeeks.org/pyqt5-how-to-set-minimum-size-of-window-setminimumsize-method/
Microsoft CoPilot (Large language model). https://copilot.microsoft.com/chats/MNy4fWeSeJRwRduBGKhgf
