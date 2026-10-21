from memory import InstructionMemory, DataMemory
from registers import RegisterFile
from control import MainControl, ALUControl
from alu import ALU

class LEGv8_CPU:
    def __init__(self, hex_file_path):
        self.pc = 0
        self.imem = InstructionMemory(hex_file_path)
        self.dmem = DataMemory()
        self.reg_file = RegisterFile()
        self.main_ctrl = MainControl()
        self.alu_ctrl = ALUControl()
        self.alu = ALU()
        self.halted = False

        self.current_instr = 0
        self.ctrl_signals = {}

    def run(self):
        cycle = 0
        print("--- Simulation Start ---")
        while not self.halted:
            self.step()
            if not self.halted:
                self.log_state(cycle)
            cycle += 1
        print("--- Simulation Halted ---")

    def step(self):
        self.current_instr = self.imem.read(self.pc)

        if self.current_instr == 0:
            self.halted = True
            return

        opcode = self.current_instr >> 21
        self.ctrl_signals = self.main_ctrl.decode(opcode)

        Rm = (self.current_instr >> 16) & 0x1F
        shamt = (self.current_instr >> 10) & 0x3F
        Rn = (self.current_instr >> 5) & 0x1F
        Rd = self.current_instr & 0x1F

        def sign_extend(val, bits):
            if (val & (1 << (bits - 1))) != 0:
                val = val - (1 << bits)
            return val

        ALU_imm = sign_extend((self.current_instr >> 10) & 0xFFF, 12)
        DT_address = sign_extend((self.current_instr >> 12) & 0x1FF, 9)
        COND_BR_address = sign_extend((self.current_instr >> 5) & 0x7FFFF, 19)
        BR_address = sign_extend(self.current_instr & 0x3FFFFFF, 26)

        read_reg1 = Rn
        if self.ctrl_signals['Reg2Loc'] or (opcode >> 3) == 180:
            read_reg2 = Rd
        else:
            read_reg2 = Rm

        reg_data1, reg_data2 = self.reg_file.read(read_reg1, read_reg2)

        if opcode == 1986 or opcode == 1984:
            imm = DT_address
        elif (opcode >> 1) == 580 or (opcode >> 1) == 836:
            imm = ALU_imm
        else:
            imm = 0

        if self.ctrl_signals['ALUSrc']:
            alu_b = imm
        else:
            alu_b = reg_data2

        alu_control = self.alu_ctrl.get_alu_control(self.ctrl_signals['ALUOp'], opcode)
        alu_result, zero_flag = self.alu.execute(reg_data1, alu_b, alu_control)

        read_data = 0
        if self.ctrl_signals['MemWrite']:
            self.dmem.write_word(alu_result, reg_data2)
        if self.ctrl_signals['MemRead']:
            read_data = self.dmem.read_word(alu_result)

        if self.ctrl_signals['MemtoReg']:
            write_data = read_data
        else:
            write_data = alu_result

        if self.ctrl_signals['RegWrite']:
            self.reg_file.write(Rd, write_data)

        if self.ctrl_signals['Branch']:
            if self.ctrl_signals['ALUOp'] == 1:
                if zero_flag:
                    self.pc = self.pc + (COND_BR_address * 4)
                else:
                    self.pc = self.pc + 4
            else:
                self.pc = self.pc + (BR_address * 4)
        else:
            self.pc = self.pc + 4

    def log_state(self, cycle):
        print(f"Cycle: {cycle}")
        print(f"PC: {self.pc}")
        print(f"Instruction: 0x{self.current_instr:08X}")

        if self.ctrl_signals:
            print("Control Signals:")
            for key, value in self.ctrl_signals.items():
                 print(f"  {key}: {value}")
        else:
            print("Control Signals: [MISSING - Check step() implementation]")

        print("Registers (Non-Zero):")
        for i in range(32):
            val = self.reg_file.read(i, 31)[0]
            if val != 0:
                print(f"  X{i}: {val}")
        print("-" * 20)
