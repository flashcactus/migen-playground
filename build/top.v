/* Machine-generated using Migen */
module top(
	output [6:0] 7seg,
	output user_led,
	output user_led_1,
	output user_led_2,
	output user_led_3,
	output user_led_4,
	output user_led_5,
	output user_led_6,
	output user_led_7,
	output user_led_8,
	output user_led_9,
	input key
);

reg [9:0] counter = 10'd0;
wire btn_clk;
reg btn_rst = 1'd0;
wire [3:0] value;
reg [6:0] digit = 7'd0;


// Adding a dummy event (using a dummy signal 'dummy_s') to get the simulator
// to run the combinatorial process once at the beginning.
// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign btn_clk = key;
assign value = counter[3:0];
assign {user_led_9, user_led_8, user_led_7, user_led_6, user_led_5, user_led_4, user_led_3, user_led_2, user_led_1, user_led} = counter;
assign 7seg = digit;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	digit <= 7'd0;
	case (value)
		1'd0: begin
			digit <= 6'd63;
		end
		1'd1: begin
			digit <= 3'd6;
		end
		2'd2: begin
			digit <= 7'd91;
		end
		2'd3: begin
			digit <= 7'd103;
		end
		3'd4: begin
			digit <= 7'd102;
		end
		3'd5: begin
			digit <= 7'd109;
		end
		3'd6: begin
			digit <= 7'd125;
		end
		3'd7: begin
			digit <= 3'd7;
		end
		4'd8: begin
			digit <= 7'd127;
		end
		4'd9: begin
			digit <= 7'd111;
		end
		4'd10: begin
			digit <= 7'd119;
		end
		4'd11: begin
			digit <= 7'd124;
		end
		4'd12: begin
			digit <= 6'd60;
		end
		4'd13: begin
			digit <= 7'd94;
		end
		4'd14: begin
			digit <= 7'd123;
		end
		4'd15: begin
			digit <= 7'd113;
		end
	endcase
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

always @(posedge btn_clk) begin
	if (btn_rst) begin
		counter <= 10'd0;
	end else begin
		counter <= (counter + 1'd1);
	end
end

endmodule
