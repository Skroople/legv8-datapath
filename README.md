# legv8-datapath

A **single-cycle LEGv8 CPU simulator** in Python. It runs machine code programs and shows how the datapath and control unit handle each instruction: fetch, decode, control signals, ALU, memory access, write-back and PC update, all in one clock cycle.

Built for a Computer Organization course, following on from [legv8-assembler](https://github.com/Skroople/legv8-assembler). The handout is in [ASSIGNMENT.md](ASSIGNMENT.md).

## How it works

| Module | Role |
|---|---|
| `cpu.py` | Simulation loop; `step()` wires the datapath for one instruction |
| `control.py` | Main control unit (opcode to `Reg2Loc`, `ALUSrc`, `MemtoReg`, `RegWrite`, `MemRead`, `MemWrite`, `Branch`, `ALUOp`) and ALU control |
| `alu.py` | ADD, SUB and pass-B (for `CBZ`), plus the Zero flag that decides the branch |
| `registers.py` | 32 × 64-bit register file; `XZR` (X31) always reads 0 |
| `memory.py` | Instruction and data memory |

Each `step()`:

1. **Fetch** the 32-bit word at `PC`. A word of `0x00000000` halts the CPU.
2. **Decode** the opcode and let the control unit set the control signals.
3. **Read registers.** `Reg2Loc` picks whether the second read register comes from `Rm` (R-format) or `Rt` (`STUR`/`CBZ`).
4. **Execute.** `ALUSrc` chooses between a register and the sign-extended immediate.
5. **Memory.** `LDUR`/`STUR` access data memory at `Rn + offset`.
6. **Write back.** `MemtoReg` chooses between ALU result and loaded value.
7. **Next PC.** `PC + 4`, or `PC + (offset << 2)` for a taken `B`/`CBZ`.

Supported instructions: `ADD`, `SUB`, `ADDI`, `SUBI`, `LDUR`, `STUR`, `CBZ`, `B`.

## Run

```bash
python run_cpu.py test_cases/test_all.hex   # cycle-by-cycle log
python auto_grade.py                        # compare all programs with reference output
```

All test programs match the reference cycle-by-cycle output (100/100).
