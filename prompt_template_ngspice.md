You aim to design a topology for a given circuit described in the text. 
Please ensure your designed circuit topology works properly and achieves the design requirements. 

Here is an example:

## Question 
Design a 2-stage amplifier (first stage: a common-source stage with current-source load, second stage: a common-source stage with resistor load).

Input node name: Vin, Vbias.

Output node name: Vout.


## Answer

### Task 1

#### Components Needed
- **NMOS Transistors**: M1 and M3
- **PMOS Transistors**: M2 (used as the current source in the first stage)
- **Resistors**: R1 for the second stage load
- **Power Supply**: Vdd for DC supply
- **Input Signal Source**: Vin, Vbias for biasing and signal input
- **Capacitors**: Not specified but can be included for coupling and bypass applications if required

#### Stage 1: Common-Source Amplifier with Current Source Load
1. **Transistor Setup**:
   - **M1** (NMOS) as the main amplifying transistor.
   - Gate of **M1** is connected to the input node **Vin**.
   - Source of **M1** connected to the ground.
   - Drain of **M1** connected to the drain of **M2**.

2. **Biasing**:
   - **Vin** provides the input signal.
   - **Vbias** is used to bias **M2** (PMOS), ensuring it operates as a current source.

3. **Current Source Load (M2)**:
   - **M2**, a PMOS transistor, is configured as a current source.
   - The source of **M2** is connected to **Vdd**, and its gate is connected to **Vbias**.
   - Drain of **M2** is connected to the drain of **M1**, providing a high-impedance load.

#### Stage 2: Common-Source Amplifier with Resistor Load
1. **Transistor Setup**:
   - **M3** (NMOS) as the main amplifying transistor for the second stage.
   - Gate of **M3** connected to the drain of **M1**.
   - Source of **M3** connected to the ground.
   - Drain of **M3** connected to **Vout** through resistor **R1**.

2. **Load and Coupling**:
   - **R1** connects the drain of **M3** to **Vdd**. This resistor converts the current through **M3** into an output voltage.

### Task 2

```
* Two-Stage Amplifier

* Define the MOSFET models
.model nmos_model nmos level=1 kp=100e-6 vto=0.5
.model pmos_model pmos level=1 kp=50e-6 vto=-0.5

* Power Supplies for the power and input signal
Vdd Vdd 0 5.0
Vin Vin 0 1.0
Vbias Vbias 0 4.0

* First Stage: Common-Source with Active Load
* parameters: name, drain, gate, source, bulk, model, w, l
M1 Drain1 Vin 0 0 nmos_model w=50e-6 l=1e-6
M2 Drain1 Vbias Vdd Vdd pmos_model w=100e-6 l=1e-6

* Second Stage: Common-Source with Resistor Load
M3 Vout Drain1 0 0 nmos_model w=100e-6 l=1e-6
R1 Vout Vdd 1k

.end
```


As you have seen, the output of your designed topology should consist of two tasks:
1. Give a detailed design plan about all devices and their interconnectivity nodes and properties.
2. Write a complete NgSpice code, describing the topology of integrated analog circuits according to the design plan. 

Please give the runnable code without any placeholders.


Do not write other redundant codes after ```.end```.

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


