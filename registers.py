class RegisterFile:
    def __init__(self):
        self.regs = [0] * 32

    def read(self, reg1, reg2):
        r1 = self.regs[reg1] if reg1 != 31 else 0
        r2 = self.regs[reg2] if reg2 != 31 else 0
        return r1, r2

    def write(self, reg, value):
        if reg != 31:
            self.regs[reg] = value & 0xFFFFFFFFFFFFFFFF
