PRINT_CLAY = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4


mem = [
    PRINT_CLAY,
    SAVE_REG, #Save 37 in R0
    0,
    37,
    PRINT_CLAY,
    HALT,
]
reg = [0] * 8 # Registers

pc = 0

running = True

while running:
    inst = mem[pc]
    if inst == PRINT_CLAY:
        print("Clay")
        pc+=1

    elif inst == SAVE_REG:
        addy = mem[pc+1]
        val = mem[pc+2]
        reg[addy] = val
        print(reg[addy])
        pc+=3
    
    elif inst == HALT:
        break

    else:
        print(f"Unknown OP{inst}")
        running = False
