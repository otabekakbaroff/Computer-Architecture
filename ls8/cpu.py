"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None]*256
        self.reg = [0]*8
        self.pc = 0
        self.fl = 0b000000

    def load(self, file_name):
        """Load a program into memory."""

        address = 0
        
        with open(file_name, 'r') as file:
          for line in file:
            split_line = line.split("#")
            command = split_line[0].strip()

            if command == '':
              continue
            
            num = int(command, 2)

            self.ram[address] = num
            
            address = address +  1
            
            
    def ram_read(self,address):
        return self.ram[address]

    def ram_write(self,address,instruction):
        self.ram[address] = instruction

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc


        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]


        elif op == "CMP":
            if reg_a == reg_b:
                # print("CMP: E : EQUAL ")
                self.fl =  0b00000001
            if reg_a < reg_b:
                # print("CMP: L : LESS THAN")
                self.fl =  0b00000100
            if reg_a > reg_b:
                # print("CMP: G : Greater Than")
                self.fl =   0b00000010

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

        self.reg[7] = 0b11110100  #Stack Pointer

        running = True

        while running:

            instruction = self.ram[self.pc]
            # print(f"instruction: {instruction}")
            if instruction == 0b00000001: # HLT
                self.pc = self.pc + (0b01000111 >> 6) + 1
                running = False

            if instruction == 0b10000010: ## LDI
                register = self.ram[self.pc+1]
                value = self.ram[self.pc+2]
                self.reg[register] = value 
                self.pc = self.pc + (0b10000010 >> 6) + 1

                


            if instruction == 0b01000111: ## PRN
                register = self.ram[self.pc+1]
                self.pc = self.pc + (0b01000111 >> 6) + 1
                print(f"PRN: {self.reg[register]}")


            if instruction == 0b10100111:  # CMP 
                registerA = self.reg[self.ram[self.pc + 1]]
                registerB = self.reg[self.ram[self.pc + 2]]
                self.alu('CMP', registerA, registerB)
                self.pc = self.pc + (0b10100111 >> 6) + 1


            if instruction == 0b01010100: # JMP
                register = self.ram[self.pc + 1]
                address = self.reg[register]
                self.pc = address
          


            if instruction == 0b01010101: # JEQ
                register = self.ram[self.pc + 1]
                equal = self.fl 
                if equal == 0b1:
                    # print("==============================HIT")
                    self.pc = self.reg[register]
                else:
                    self.pc = self.pc + (0b01000111 >> 6) + 1

            if instruction == 0b01010110: # JNE
                register = self.ram[self.pc + 1]
                e = self.fl 
                if e != 0b1:
                    self.pc = self.reg[register]
                else:
                    self.pc = self.pc + (0b01000111 >> 6) + 1





