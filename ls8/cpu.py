"""CPU functionality."""

import sys

global HLT
HLT = 0b0000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while self.pc < len(self.ram):
            ir = self.pc
            instruction = self.ram_read(ir)
            try:
                operand_a, operand_b = self.ram_read(ir + 1), self.ram_read(ir + 2)
            except IndexError:
                operand_a, operand_b = None, None

            if instruction == HLT:
                break
            elif instruction == 0b10000010:
                self.LDI(operand_a, operand_b)
                self.pc += 1
            elif instruction == 0b01000111:
                self.PRN(operand_a)
                self.pc += 1
            else:
                self.pc += 1



    def LDI(self, address, value):
        self.reg[address] = value

    def PRN(self, address):
        print(self.reg[address])