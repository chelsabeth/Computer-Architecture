"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes of memory 
        self.reg = [0] * 8 # 8 general-purpose registers R0-R7
        self.reg[7] = 0xF4
        self.pc = 0 
        self.fl = '00000000'

    def LDI(self, reg, immediate):
        self.reg[reg] = immediate 

    def PRN(self, reg):
        print(self.reg[reg])

    def HLT(self):
        exit()

    def POP(self, reg):
        addr_to_pop_from = self.reg[7]
        value = self.ram_read(addr_to_pop_from)

        reg_num = self.ram_read(self.pc + 1)
        self.reg[reg_num] = value

        self.reg[7] += 1
        

    def PUSH(self, reg):
        self.reg[7] -= 1

        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        addr_to_push_to = self.reg[7]
        self.ram_write(value, addr_to_push_to)

    def CALL(self, reg):
        return_addr = self.pc + 2 

        self.reg[7] -= 1
        addr_to_push_to = self.reg[7]
        self.ram_write(return_addr, addr_to_push_to)

        reg_num = self.ram_read(self.pc + 1)
        subroutine_addr = self.reg[reg_num]

        self.pc = subroutine_addr

    def RET(self):
        addr_to_pop_from = self.reg[7]
        return_addr = self.ram_read(addr_to_pop_from)
        self.reg[7] += 1

        self.pc = return_addr

    def ADD(self, reg_a, reg_b):
        self.alu('ADD', reg_a, reg_b)

    def JMP(self, reg):
        self.pc = self.reg[reg]

    def JEQ(self, reg):
        if self.fl[7] == '1':
            self.pc = self.reg[reg] 
        else:
            self.pc += 2

    def JNE(self, reg):
        if self.fl[7] == '0':
            self.pc = self.reg[reg]
        else:
            self.pc += 2

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#",1)[0]
                        line = int(line, 2) # int() is base 10 by default, so I had to change it to binary base 2
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            value1 = self.reg[reg_a]
            value2 = self.reg[reg_b]
            if value1 < value2:
                self.fl = '00000100'
            elif value1 > value2:
                self.fl = '00000010'
            elif value1 == value2:
                self.fl = '00000001'
        else:
            raise Exception("Unsupported ALU operation")
        
    def MUL(self, a, b):
        self.alu('MUL', a, b)

    def CMP(self, a, b):
        self.alu('CMP', a, b)

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
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
        running = True

        fix_my_run = {
            '0b00000001': self.HLT,
            '0b10000010': self.LDI,
            '0b01000111': self.PRN,
            '0b10100010': self.MUL,
            '0b01000101': self.PUSH,
            '0b01000110': self.POP,
            '0b10100000': self.ADD,
            '0b01010000': self.CALL,
            '0b00010001': self.RET,
            '0b10100111': self.CMP,
            '0b01010100': self.JMP,
            '0b01010101': self.JEQ,
            '0b01010110': self.JNE
        }

        while running:
            ir = self.ram_read(self.pc)
            op_1 = self.ram_read(self.pc+1)
            op_2 = self.ram_read(self.pc+2)

            instBinString = format(ir, '#010b')
            arguments = instBinString[2:4]
            alu_op = instBinString[4]
            sets_pc = instBinString[5]
            inst_id = instBinString[6:]
            if instBinString in fix_my_run:
                function = fix_my_run[instBinString]
                if arguments == "00":
                    function()
                    if sets_pc == '0':
                        self.pc += 1
                elif arguments == "01":
                    function(op_1)
                    if sets_pc == '0':
                        self.pc += 2
                elif arguments == "10":
                    function(op_1, op_2)
                    if sets_pc == '0':
                        self.pc += 3


