class MainControl:
    def decode(self, opcode):
        signals = {
            'Reg2Loc': False, 'Branch': False, 'MemRead': False,
            'MemtoReg': False, 'ALUOp': 0, 'MemWrite': False,
            'ALUSrc': False, 'RegWrite': False
        }

        if opcode == 1112 or opcode == 1624:
            signals['RegWrite'] = True
            signals['ALUOp'] = 2
        elif (opcode >> 1) == 580 or (opcode >> 1) == 836:
            signals['ALUSrc'] = True
            signals['RegWrite'] = True
            signals['ALUOp'] = 2
        elif opcode == 1986:
            signals['ALUSrc'] = True
            signals['MemtoReg'] = True
            signals['RegWrite'] = True
            signals['MemRead'] = True
            signals['ALUOp'] = 0
        elif opcode == 1984:
            signals['ALUSrc'] = True
            signals['MemWrite'] = True
            signals['Reg2Loc'] = True
            signals['ALUOp'] = 0
        elif (opcode >> 3) == 180:
            signals['Branch'] = True
            signals['Reg2Loc'] = False
            signals['ALUOp'] = 1
        elif (opcode >> 5) == 5:
            signals['Branch'] = True
            signals['ALUOp'] = 0

        return signals


class ALUControl:
    def get_alu_control(self, alu_op, opcode):
        if alu_op == 0:
            return 2
        elif alu_op == 1:
            return 7
        elif alu_op == 2:
            if (opcode >> 1) == 580 or opcode == 1112:
                return 2
            elif (opcode >> 1) == 836 or opcode == 1624:
                return 6
        return 0
