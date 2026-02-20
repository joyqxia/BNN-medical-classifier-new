import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles

@cocotb.test()
async def test_bnn_classifier(dut):
    """Test the BNN hardware against our medical patient data."""
    
    # 1. Start the hardware clock (50 MHz / 20ns period)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    # 2. Reset the chip before sending data
    dut.rst_n.value = 0 # Pull reset low
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1 # Release reset
    
    # Enable the design
    dut.ena.value = 1

    # 3. THE PATIENT DATA (From the ML Model)
    # Format: (8-bit patient vitals, Expected Diagnosis Flag)
    test_cases = [
        (0b11010011, 1),  # Patient 1
        (0b00001000, 0),  # Patient 2
        (0b10111111, 1),  # Patient 3
    ]

    # 4. RUN THE SIMULATION
    dut._log.info("Starting Patient Data Simulation...")
    
    for patient_data, expected_diagnosis in test_cases:
        # Feed the 8-bit patient data into the 8 input pins
        dut.ui_in.value = patient_data
        
        # Wait for one clock cycle for the Verilog logic gates to process
        await FallingEdge(dut.clk)
        
        # Read the first output pin (uo_out[0])
        hardware_prediction = dut.uo_out[0].value
        
        # Log it to the terminal so the judges can see it working!
        dut._log.info(f"Vitals IN: {bin(patient_data)} | Hardware OUT: {hardware_prediction} | Expected: {expected_diagnosis}")
        
        # 5. THE PROOF: If the hardware gets it wrong, the test fails immediately.
        assert hardware_prediction == expected_diagnosis, f"Hardware failed on data {bin(patient_data)}!"

    dut._log.info("All patients classified successfully. Hardware verified!")
