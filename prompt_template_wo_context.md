You aim to design a topology for a given circuit described in the text. 
Please ensure your designed circuit topology works properly and achieves the design requirements. 

The output of your designed topology should consist of two tasks:
1. Give a detailed design plan about all devices and their interconnectivity nodes and properties.
2. Write a complete Python code, describing the topology of integrated analog circuits according to the design plan. 

Please make sure your Python code is compatible with PySpice. 
Please give the runnable code without any placeholders.


Do not write other redundant codes after ```simulator = circuit.simulator()```.

For importing libraries, you can use:
```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
```


For the mosfet, you can refer to the following code:
```python
circuit.model('nmos_model', 'nmos', level=1, kp=100e-6, vto=0.5)
circuit.model('pmos_model', 'pmos', level=1, kp=50e-6, vto=-0.5)
circuit.MOSFET('1', 'Vout', 'Vin', circuit.gnd, circuit.gnd, model='nmos_model', w=50e-6, l=1e-6)
```

For the resistor and the voltage source, you can can refer to the following code:
```python
circuit.R('1', 'Vout', 'Vdd', 1@u_kΩ)
circuit.V('dd', 'Vdd', circuit.gnd, 5.0)
```

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


