You aim to design a topology for a given circuit described in the text. 
Please ensure your designed circuit topology works properly and achieves the design requirements. 

Here is an example:

## Question 
Design a 2-stage amplifier (first stage: a common-source stage with current-source load, second stage: a common-source stage with resistor load).

Input node name: Vin, Vbias.

Output node name: Vout.


## Answer

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Two-Stage Amplifier')
# Define the MOSFET models
circuit.model('nmos_model', 'nmos', level=1, kp=100e-6, vto=0.5)
circuit.model('pmos_model', 'pmos', level=1, kp=50e-6, vto=-0.5)

# Power Supplies for the power and input signal

circuit.V('dd', 'Vdd', circuit.gnd, 5.0) # 5V power supply
circuit.V('in', 'Vin', circuit.gnd, 1.0) # 1V input for bias voltage (= V_th + 0.5 = 0.5 + 0.5 = 1.0)
circuit.V('bias', 'Vbias', circuit.gnd, 4.0) # 4V input for bias voltage (= Vdd - |V_th| - 0.5 = 5.0 - 0.5 - 0.5 = 4.0)

# First Stage: Common-Source with Active Load
# parameters: name, drain, gate, source, bulk, model, w, l
circuit.MOSFET('1', 'Drain1', 'Vin', circuit.gnd, circuit.gnd, model='nmos_model', w=50e-6, l=1e-6)
circuit.MOSFET('2', 'Drain1', 'Vbias', 'Vdd', 'Vdd', model='pmos_model', w=100e-6, l=1e-6)

# Second Stage: Common-Source with Resistor Load
circuit.MOSFET('3', 'Vout', 'Drain1', circuit.gnd, circuit.gnd, model='nmos_model', w=100e-6, l=1e-6)
circuit.R('1', 'Vout', 'Vdd', 1@u_kΩ)

# Analysis Part
simulator = circuit.simulator()
```


As you have seen, the output of your designed topology should be in a complete Python code, describing the topology of integrated analog circuits according to the design plan. 

Please make sure your Python code is compatible with PySpice. 
Please give the runnable code without any placeholders.


Do not write other redundant codes after ```simulator = circuit.simulator()```.

There are some tips you should remember all the time:
1. For the MOSFET definition circuit.MOSFET(name, drain, gate, source, bulk, model, w=w1,l=l1), be careful about the parameter sequence. 
2. You should connect the bulk of a MOSFET to its source.
3. Please use the MOSFET threshold voltage, when setting the bias voltage.
4. Avoid giving any AC voltage in the sources, just consider the operating points.
5. Make sure the input and output node names appear in the circuit.
6. Avoid using subcircuits.
7. Use nominal transistor sizing.
8. Assume the Vdd = 5.0 V.

## Question

Design [TASK].

Input node name: [INPUT].

Output node name: [OUTPUT].


## Answer


