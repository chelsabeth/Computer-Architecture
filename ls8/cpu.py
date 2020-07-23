"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes of memory 
        self.reg = [0] * 8 # 8 general-purpose registers R0-R7
        self.pc = 0 
        # self.ir = 0
        # self.MAR = 0
        # self.MDR = 0
        # self.FL = 0

    def LDI(self, reg, immediate):
        # set the value of a register to an integer
        self.reg[reg] = immediate 

    def PRN(self, reg):
        # print numeric value stored in the given register 
        # print in the console the decimal integer value that is stored in the given register
        print(self.reg[reg])

    def HLT(self):
        # halt the CPU
        exit()

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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, write, address):
        self.ram[address] = write
    

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # read the memory address that's stored in pc and store the result in ir
            ir = self.ram_read(self.pc) 
            # using ram_read(), read the bytes at pc+1 and pc+2
            # from RAM into variables operand_a and operand_b
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            instBinString = format(ir, '#010b')
            # console log instBinString
            # set the pc according 

            operands_count = instBinString[2:3]
            alu_op = instBinString[4]
            sets_pc = instBinString[5]
            inst_id = instBinString[6:]

            if inst_id == '0001':
                self.HLT()
            elif inst_id == '0010':
                self.LDI(operand_a, operand_b)
                self.pc += 3
            elif inst_id == '0111':
                self.PRN(operand_a)
                self.pc += 2

                # PRN, LDI and string problem 



        # with an if else cascade, go through the bits it give you and decide what instructions you should do

