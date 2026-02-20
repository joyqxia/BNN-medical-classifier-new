<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Neuro-Kinematic is a hardware-accelerated Application-Specific Integrated Circuit (ASIC) designed to diagnose heart disease entirely on-chip. 

Instead of relying on a power-hungry CPU or cloud connection, we synthesized a Binarized Neural Network (BNN) directly into physical logic gates. The hardware takes 8 thresholded biometric markers from the Cleveland Heart Disease dataset. It processes these inputs through parallel XNOR gates (representing our quantized PyTorch weights) and a physical adder tree (Popcount). If the patient's match score hits the binarized threshold, the hardware flags the diagnosis in a single clock cycle.

## How to test

To test the chip, provide an 8-bit binary input to the dedicated input pins (`ui_in[7:0]`). Each pin corresponds to a specific thresholded medical feature:

* `ui_in[0]`: Age (> 50 years)
* `ui_in[1]`: Resting Blood Pressure (> 140 mmHg)
* `ui_in[2]`: Cholesterol (> 240 mg/dl)
* `ui_in[3]`: Max Heart Rate (< 100 bpm)
* `ui_in[4]`: Chest Pain Type (Asymptomatic/Typical)
* `ui_in[5]`: Exercise Induced Angina (Yes)
* `ui_in[6]`: Oldpeak ST Depression (> 1.5)
* `ui_in[7]`: Sex (Male)

Once the input is provided, the chip will immediately evaluate the data. Read the first dedicated output pin (`uo_out[0]`). 
* A reading of `1` indicates High Risk of heart disease. 
* A reading of `0` indicates Healthy.

## External hardware

No complex external microcontrollers are required. To physically test this chip once manufactured, you only need a standard 8-position DIP switch to manually toggle the patient vitals (inputs) and a single LED connected to `uo_out[0]` to display the diagnostic result.
