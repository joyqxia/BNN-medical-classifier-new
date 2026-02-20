# Neuro-Kinematic BNN Medical Classifier

[![GDS Badge](../../workflows/gds/badge.svg)](../../workflows/gds/badge.svg)
[![Docs Badge](../../workflows/docs/badge.svg)](../../workflows/docs/badge.svg)
[![Test Badge](../../workflows/test/badge.svg)](../../workflows/test/badge.svg)
[![FPGA Badge](../../workflows/fpga/badge.svg)](../../workflows/fpga/badge.svg)

**Hardware-accelerated medical diagnosis using a Binarized Neural Network (BNN) ASIC**

## Overview

We took a raw medical dataset, trained a quantized neural network, and successfully translated it into a fully verifiable, manufacturable silicon chip. This project demonstrates the complete pipeline from machine learning model training to hardware implementation, creating a low-power, high-speed medical diagnostic ASIC that operates entirely on-chip without requiring cloud connectivity or complex external processors.

## What is Neuro-Kinematic?

Neuro-Kinematic is a hardware-accelerated Application-Specific Integrated Circuit (ASIC) designed to diagnose heart disease entirely on-chip. Instead of relying on a power-hungry CPU or cloud connection, we synthesized a Binarized Neural Network (BNN) directly into physical logic gates.

The hardware takes 8 thresholded biometric markers from the Cleveland Heart Disease dataset and processes them through parallel XNOR gates (representing quantized PyTorch weights) and a physical adder tree (Popcount). If the patient's match score hits the binarized threshold, the hardware flags the diagnosis in a single clock cycle at 50 MHz.

## How It Works

### Architecture

1. **Input Processing**: 8-bit binary input representing thresholded medical features
2. **Weight Comparison**: Parallel XNOR gates compare inputs against trained binary weights
3. **Popcount**: Adder tree counts matching features
4. **Threshold Activation**: Binary decision based on match score
5. **Output**: Single-bit diagnostic flag (High Risk = 1, Healthy = 0)

### Technical Details

- **Clock Frequency**: 50 MHz
- **Latency**: Single clock cycle inference
- **Power Efficiency**: Ultra-low power consumption (no CPU/cloud required)
- **Technology**: Synthesized to standard cell library via LibreLane

## Pin Configuration

### Inputs (`ui_in[7:0]`)

| Pin | Feature | Threshold |
|-----|---------|-----------|
| `ui_in[0]` | Age | > 50 years |
| `ui_in[1]` | Resting Blood Pressure | > 140 mmHg |
| `ui_in[2]` | Cholesterol | > 240 mg/dl |
| `ui_in[3]` | Max Heart Rate | < 100 bpm |
| `ui_in[4]` | Chest Pain Type | Asymptomatic/Typical |
| `ui_in[5]` | Exercise Induced Angina | Yes |
| `ui_in[6]` | Oldpeak ST Depression | > 1.5 |
| `ui_in[7]` | Sex | Male |

### Outputs (`uo_out[0]`)

- `uo_out[0] = 1`: High Risk of heart disease detected
- `uo_out[0] = 0`: Healthy (low risk)

## Testing

### Simulation Testing

Run the testbench to verify functionality:

```bash
cd test
make
```

### Hardware Testing

Once manufactured, the chip can be tested with minimal external hardware:

- **Input**: Standard 8-position DIP switch connected to `ui_in[7:0]`
- **Output**: Single LED connected to `uo_out[0]` to display diagnostic result
- **No microcontrollers required**: The chip operates independently

### Test Procedure

1. Set the 8 DIP switches according to patient vitals (1 = threshold exceeded, 0 = normal)
2. Observe the LED output:
   - **LED ON** = High risk of heart disease
   - **LED OFF** = Healthy/low risk

## Project Structure

```
BNN-medical-classifier-new/
├── src/
│   ├── project.v          # Main Verilog implementation
│   └── config.json        # Configuration files
├── test/
│   ├── tb.v              # Testbench
│   ├── test.py           # Python test script
│   └── Makefile          # Build configuration
├── docs/
│   └── info.md           # Detailed project documentation
├── info.yaml             # Tiny Tapeout project configuration
└── README.md             # This file
```

## Future Development: Long-Term Disease Predictor

### Vision

We are expanding this project into a **Long-Term Disease Predictor** that will:

- Read entered symptoms and bodily measurements
- Predict multiple long-term diseases (streamlined to highly/moderately predictable conditions)
- Output comprehensive health assessments including:
  - Adverse health outcomes as a function of age
  - Disease severity predictions
  - Mortality risk assessment
  - Probability of full recovery

### Implementation Roadmap

**Current State**: Hardware description language implementation on-chip

**Next Steps**:
1. **Integration**: Connect chip to medical devices and databases for real-time patient analysis
2. **Privacy**: Implement on-chip data processing to prevent patient data exposure
3. **Scalability**: Expand model to support multiple disease classifications

### Design Tradeoffs

- **Input Size & Breadth**: Increasing input features and training for more diseases improves comprehensiveness but increases complexity and latency
- **Disease Coverage**: Reduced disease set improves performance and predictability
- **Dataset Breadth**: Larger training datasets improve accuracy but require more hardware resources
- **Privacy vs. Functionality**: On-chip processing enhances privacy but limits cloud-based model updates

### Privacy Considerations

The ASIC architecture inherently protects patient privacy by:
- **On-chip Processing**: All inference happens locally; no data leaves the device
- **No External Communication**: No network connectivity required
- **Minimal Data Storage**: Only thresholded binary features are processed
- **Future Enhancements**: Additional encryption and secure data handling protocols planned

## Development

### Prerequisites

- Verilog simulator (Icarus Verilog, Verilator, or similar)
- Python 3.x (for test scripts)
- Make

### Building Locally

```bash
# Run tests
cd test
make

# View waveforms (if using GTKWave)
gtkwave tb.gtkw
```

### Tiny Tapeout Integration

This project is designed for [Tiny Tapeout](https://tinytapeout.com), an educational platform that makes ASIC manufacturing accessible. The design is automatically synthesized and verified through GitHub Actions using LibreLane.

## Authors

**Sheraz, Joy, Philip & Subodh**

## License

See [LICENSE](LICENSE) file for details.

## Resources

- [Project Documentation](docs/info.md)
- [Tiny Tapeout Documentation](https://tinytapeout.com)
- [LibreLane Documentation](https://www.zerotoasiccourse.com/terminology/librelane/)
- [Cleveland Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease)

## Acknowledgments

Built as part of the Tiny Tapeout educational ASIC program. Special thanks to the open-source hardware community for making accessible chip design possible.

---

**GitHub**: [github.com/joyqxia/BNN-medical-classifier-new](https://github.com/joyqxia/BNN-medical-classifier-new)
