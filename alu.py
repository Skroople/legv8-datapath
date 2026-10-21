class ALU:
    def execute(self, operand_a, operand_b, alu_control):
        result = 0
        zero_flag = False

        if alu_control == 2:
            result = operand_a + operand_b
        elif alu_control == 6:
            result = operand_a - operand_b
        elif alu_control == 7:
            result = operand_b

        result &= 0xFFFFFFFFFFFFFFFF

        if result == 0:
            zero_flag = True

        return result, zero_flag
