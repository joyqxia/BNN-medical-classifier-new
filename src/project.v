`default_nettype none

module tt_um_bnn_classifier (
    input  wire [7:0] ui_in,    // Dedicated inputs (Our 8 medical vitals)
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path 
    input  wire       ena,      // always 1 when the design is powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // 1. THE HARDCODED AI WEIGHTS (From PyTorch Model)
    wire [7:0] trained_weights = 8'b11110011; 

    // 2. THE NEURAL NETWORK MULTIPLICATION (XNOR Gate)
    wire [7:0] xnor_result = ~(ui_in ^ trained_weights);

    // 3. THE POPCOUNT (Adder Tree)
    wire [3:0] match_score = xnor_result[0] + xnor_result[1] + 
                             xnor_result[2] + xnor_result[3] + 
                             xnor_result[4] + xnor_result[5] + 
                             xnor_result[6] + xnor_result[7];

    // 4. THE ACTIVATION THRESHOLD
    wire high_risk_detected = (match_score >= 4'd4) ? 1'b1 : 1'b0;

    // 5. ASSIGN OUTPUT PINS
    assign uo_out[0] = high_risk_detected;
    
    // Explicitly tie off all unused pins to 0 to prevent synthesis routing errors
    assign uo_out[7:1] = 7'b0000000;
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // 6. SUPPRESS UNUSED SIGNAL WARNINGS
    wire _unused = &{ena, clk, rst_n, uio_in, 1'b0};

endmodule
