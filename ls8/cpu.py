"""CPU functionality."""


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        self.flags = [0] * 8

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""

        address = 0

        file = open(file, 'r')
        program = file.readlines()

        for instruction in program:
            if instruction[0] != "#" and instruction != '\n':
                instruction = instruction[:8]
                self.ram[address] = int(instruction, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flags[7] = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flags[5] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags[6] = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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
            num_operands = instruction >> 6
            if instruction == 0b0001:
                # HLT
                break
            operand_a = None
            operand_b = None
            sets_pc_directly = ((instruction >> 4) & 0b001) == 0b001
            if num_operands == 2:
                operand_a = self.ram_read(ir + 1)
                operand_b = self.ram_read(ir + 2)
            elif num_operands == 1:
                operand_a = self.ram_read(ir + 1)
            if instruction == 0b10000010:
                self.LDI(operand_a, operand_b)
            elif instruction == 0b10100000:
                self.alu("ADD", operand_a, operand_b)
            elif instruction == 0b01000111:
                self.PRN(operand_a)
            elif instruction == 0b10100010:
                self.alu('MUL', operand_a, operand_b)
            elif instruction == 0b01000101:
                self.PUSH(operand_a)
            elif instruction == 0b01000110:
                self.POP(operand_a)
            elif instruction == 0b01010000:
                self.CALL(operand_a)
            elif instruction == 0b00010001:
                self.RET()
            elif instruction == 0b10000100:
                self.ST(operand_a, operand_b)
            elif instruction == 0b01010100:
                self.JMP(operand_a)
            elif instruction == 0b10100111:
                self.alu("CMP", operand_a, operand_b)
            if not sets_pc_directly:
                self.pc += (1 + num_operands)


    def LDI(self, address, value):
        self.reg[address] = value

    def PRN(self, address):
        print(self.reg[address])

    def PUSH(self, register_address):
        self.reg[7] -= 1
        value = self.reg[register_address]
        SP = self.reg[7]
        self.ram_write(SP, value)

    def POP(self, register_address):
        SP = self.reg[7]
        value = self.ram_read(SP)
        self.reg[register_address] = value
        self.reg[7] += 1

    def CALL(self, register_address):
        next_instruction_address = self.pc + 2
        self.reg[7] -= 1
        SP = self.reg[7]
        self.ram_write(SP, next_instruction_address)
        jump_to = self.reg[register_address]
        self.pc = jump_to

    def RET(self):
        SP = self.reg[7]
        return_address = self.ram_read(SP)
        self.reg[7] += 1
        self.pc = return_address

    def ST(self, registerA, registerB):
        value = self.reg[registerB]
        address = self.reg[registerA]
        self.ram_write(address, value)

    def JMP(self, register_address):
        self.pc = self.reg[register_address]

