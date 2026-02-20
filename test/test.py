import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles

@cocotb.test()
async def test_bnn_classifier(dut):
    """Test the BNN hardware against our Cleveland Heart Disease patient data."""
    
    # 1. Start the hardware clock (50 MHz / 20ns period)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    # 2. Reset the chip before sending data
    dut.rst_n.value = 0 # Pull reset low
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1 # Release reset
    
    # Enable the design
    dut.ena.value = 1

    # 3. THE PATIENT DATA (Generated from Sherry's thresholding script)
    # Format: (0b[Age, BP, Chol, MaxHR, CP, Exang, Oldpeak, Sex], Expected_Diagnosis)
    test_cases = [
        (0b11010011, 1),  # Patient 1 (High Risk)
        (0b00001000, 0),  # Patient 2 (Healthy)
        (0b10111111, 1),  # Patient 3 (High Risk)
    ]

    # 4. RUN THE SIMULATION
    dut._log.info("Starting Patient Data Simulation...")
    
    for patient_data, expected_diagnosis in test_cases:
        # Feed the 8-bit patient data into the 8 input pins
        dut.ui_in.value = patient_data
        
        # Wait for one clock cycle for the Verilog logic gates to process
        await FallingEdge(dut.clk)
        
        # Read the first output pin (uo_out[0])
        # Give the gates one more cycle to settle, then read as a string
        await ClockCycles(dut.clk, 1)
        output_str = dut.uo_out.value.binstr
        hardware_prediction = 1 if output_str[-1] == '1' else 0
        
        # Log results
        dut._log.info(f"Vitals IN: {bin(patient_data)} | Hardware OUT: {hardware_prediction} | Expected: {expected_diagnosis}")
        
        # 5. THE PROOF
        assert hardware_prediction == expected_diagnosis, f"Hardware failed on data {bin(patient_data)}!"

    dut._log.info("All patients classified successfully. Hardware verified!")
