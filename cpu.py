"""CPU functionality."""
# LDI: load "immediate", store a value in a register, or "set this register to this value".
# PRN: a pseudo-instruction that prints the numeric value stored in a register.
# HLT: halt the CPU and exit the emulator.
import sys

# setup consts for op codes
LDI = 0b10000010 # LDI R0,8 130
PRN = 0b01000111 # PRN R0, 71
HLT = 0b00000001 # HLT
MUL = 0b10100010 # Multiply
ADD = 0b10100000 # Addition
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000

SP = 7  # stack pointer set to be used a R7 per spec

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create 256 bites of memory
        self.ram = [0] * 256
        # 8 bit register
        self.reg = [0] * 8
        # program counter PC
        self.pc = 0

    # Inside the CPU, there are two internal registers used for memory operations: 
    # the Memory Address Register (MAR) and the Memory Data Register (MDR).
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr


    def load(self, file_name):
        """Load a program into memory."""
        try:
            address = 0
            # open the file
            with open(file_name) as f:
                for line in f:
                    # strip out the white space at a inline comment
                    clean_line = line.strip().split('#')
                    # grab string number
                    value = clean_line[0].strip()

                    # check if val is blank or not, if it is skip to next line
                    if value != '':
                        # number string to integer
                        num = int(value, 2) # we need to convert a binary string to a number ex. "100000010"
                        self.ram[address] = num
                        address += 1
                    else:
                        continue

        except FileNotFoundError:
            print("ERR: FILE NOT FOUND")
            sys.exit(2)



    def alu(self, op, reg_a, reg_b): # arithmetic logic unit ALU
        """ALU operations."""

        if op == "ADD": # addition
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": # subtraction 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL': # multiplication
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV': # division 
            self.reg[reg_a] /= self.reg[reg_b]
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

    def run(self, file_name):
        """Run the CPU."""
        # load the program into the memory
        self.load(file_name)

        # run the program
        while True:
            pc = self.pc # program counter
            # que the operation to start at default 0
            op = self.ram_read(pc)

            if op == LDI:
                self.reg[self.ram_read(pc + 1)] = self.ram_read(pc + 2)
                self.pc += 3
            elif op == PRN:
                print(self.reg[self.ram_read(pc + 1)])
                self.pc += 2

            # multiply
            elif op == MUL:
                # access two registers and multiply
                # get the RAM values that hold the register index we need
                a = self.ram_read(pc + 1)
                b = self.ram_read(pc + 2)
                # call the ALU
                self.alu('MUL', a, b)
                # move program counter
                self.pc += 3

            # addition
            elif op == ADD:
                # access two registers and add them
                a = self.ram_read(pc + 1)
                b = self.ram_read(pc + 2)
                # call the ALU
                self.alu('ADD', a, b)
                self.pc += 3

            # system stack
            elif op == PUSH:
                # decrement SP
                self.reg[SP] -= 1
                # get the current mem address SP points to
                stack_address = self.reg[SP]
                # get a register number from the instruction
                register_num = self.ram_read(pc + 1)
                # get value out of the register
                value = self.reg[register_num]
                # write the register value to a position in the stack
                self.ram_write(stack_address, value)
                self.pc += 2

            # # system stack
            elif op == POP:
                # get the value from the memory
                stack_value = self.ram_read(self.reg[SP])
                # get the register number from instruction in memory
                register_num = self.ram_read(pc + 1)
                # set the value of a register to the value held in the stack
                self.reg[register_num] = stack_value
                # increment SP
                self.reg[SP] += 1
                self.pc += 2

            # Subroutine Calls
            elif op == CALL:
                # decrement the SP
                self.reg[SP] -= 1
                # get the current mem address that SP points to
                stack_address = self.reg[SP]
                # get return memory address
                returned_address = pc + 2
                # add return address to the stack
                self.ram_write(stack_address, returned_address)
                # set PC to the value in register
                register_num = self.ram_read(pc + 1)
                self.pc = self.reg[register_num]

            elif op == RET:
                # pop return memory address off the stack
                # store poped memory address in the PC
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                
            elif op == HLT:
                sys.exit(1)

            else:
                print('ERR: UNKNOWN INPUT:\t', op)
                sys.exit(1)


if len(sys.argv) == 2:
    file_name = sys.argv[1]

    c = CPU()
    c.run(file_name)
else:
    # err message
    print("""
ERR: PLEASE PROVIDE A FILE NAME\n
ex python cpu.py examples/FILE_NAME
""")
    sys.exit(2)

# file_name = 'examples/print8.ls8'

# c = CPU()

# c.run(file_name)


# file_name = sys.argv[1]
# 


