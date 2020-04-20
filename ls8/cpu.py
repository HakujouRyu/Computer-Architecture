"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.running = True
        
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val
    
    def _print(self, address):
        print(f"_printing : {self.ram_read(address)}")
    
    def halt(self):
        self.running = False

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
        """Run the CPU."""
        self.instruction_set = {
            0b10000010: {"length": 3, "func": self.ram_write},
            0b01000111: {"length": 2, "func": self._print},
            0b00000001: {"length": 1, "func": self.halt}
        }

        while self.running:
            self.load()
            if self.pc >= 252: # THIS NEED TO BE FIXED! (STACK< PROLLY)
                print("max depth exceeded")
                self.halt()
            IR = self.ram[self.pc]
            increment = 1
            operand_a = None
            operand_b = None
            

            todo = self.instruction_set.get(IR, None)

            if not todo: 
                print(f"Unknown Instruction: {IR}")
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
            
            self.pc += increment

test = CPU()
test.run()
