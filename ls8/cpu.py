"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #Memory
        self.pc = 0 #Program Counter
        self.running = True
        self.reg = [0] * 8 #Registera
        self.SP = 7
        self.reg[self.SP] = 0xF4 #Stack pointer
        self.fl = None
        self.IR = None
        
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val
    
    def ldi(self, address, val):
        self.reg[address] = val
        self.pc += 3

    def _print(self, address):
        print(f"_printing : {self.reg[address]}")
        self.pc += 2
    
    def halt(self):
        self.running = False

    def mul(self, reg_a, reg_b):
        self.pc += 3
        return self.alu("MUL", reg_a, reg_b)

    def add(self, reg_a, reg_b):
        self.pc += 3
        return self.alu("ADD", reg_a, reg_b)

    def push(self, reg_a):
        self.SP -= 1
        self.ram[self.SP] = self.reg[reg_a]
        self.pc += 2

    def pop(self, reg_a):
        self.reg[reg_a] = self.ram[self.SP]
        self.SP += 1
        self.pc += 2
    
    def call(self, reg_a):
        self.fl = self.pc + 2
        self.SP -= 1
        self.ram[self.reg[self.SP]] = self.fl
        self.pc = self.reg[reg_a]


    def ret(self):
        self.pc = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        
    
    def load(self, program_filename):
        """Load a program into memory."""

        address = 0

        with open(program_filename) as f:
        # with open('ls8/examples/call.ls8') as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line, 2)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]        
        elif op =="MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        """Run the CPU."""
        self.instruction_set = {
            0b10000010: {"length": 3, "func": self.ldi, "name": 'ldi'},
            0b01000111: {"length": 2, "func": self._print, "name": '_print'},
            0b00000001: {"length": 1, "func": self.halt, "name": 'halt'},
            0b10100010: {"length": 3, "func": self.mul, "name": 'mul'},
            0b10100000: {"length": 3, "func": self.add, "name": 'add'},
            0b01000101: {"length": 2, "func": self.push, "name": 'push'},
            0b01000110: {"length": 2, "func": self.pop, "name": 'pop'},
            0b01010000: {"length": 2, "func": self.call, "name": 'call'},
            0b00010001: {"length": 1, "func": self.ret, "name": 'ret'},
        }

        while self.running:
            
            if self.pc >= 252: # THIS NEED TO BE FIXED! (STACK< PROLLY)
                print("max depth exceeded")
                self.halt()

            self.IR = self.ram[self.pc]
            increment = 1
            # inst_len = ((self.IR & 0b11000000) >> 6) + 1
            operand_a = None
            operand_b = None
            

            todo = self.instruction_set.get(self.IR, None)

            if not todo: 
                print(f"Unknown Instruction: {self.IR}")
            else:
                if todo["length"] == 3:
                    operand_a = self.ram[self.pc+1]
                    operand_b = self.ram[self.pc+2]
                    increment = 3
                    todo["func"](operand_a, operand_b)
                    

                elif todo["length"] == 2:
                    operand_a = self.ram[self.pc+1]
                    increment = 2
                    todo["func"](operand_a)
                else:
                    todo["func"]()
            

