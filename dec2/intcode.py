import itertools

intcode = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,6,23,2,23,13,27,1,27,5,31,2,31,10,35,1,9,35,39,1,39,9,43,2,9,43,47,1,5,47,51,2,13,51,55,1,55,9,59,2,6,59,63,1,63,5,67,1,10,67,71,1,71,10,75,2,75,13,79,2,79,13,83,1,5,83,87,1,87,6,91,2,91,13,95,1,5,95,99,1,99,2,103,1,103,6,0,99,2,14,0,0]

intcode[1] = 12
intcode[2] = 2

def executeOpcode(opcode: int, intcode: list, currentPosition: int):
    if opcode == 1:
        intcode[intcode[currentPosition + 3]] = intcode[intcode[currentPosition + 1]] + intcode[intcode[currentPosition + 2]]
        return intcode, False
    elif opcode == 2:
        intcode[intcode[currentPosition + 3]] = intcode[intcode[currentPosition + 1]] * intcode[intcode[currentPosition + 2]]
        return intcode, False
    else:
        return intcode, True


def executeIntcode(intcode: list):
    reachedExitOpcode = False
    currentPosition = 0
    while not reachedExitOpcode:
        intcode, reachedExitOpcode = executeOpcode(intcode[currentPosition], intcode, currentPosition)
        currentPosition += 4
    return intcode

def checkRangeOfInput(intcode: list, nounRange: int, verbRange: int):
    initialIntcode = intcode
    for noun, verb in itertools.product(range(nounRange), range(verbRange)):
        intcode[1] = noun
        intcode[2] = verb
        res = executeIntcode(intcode)
        if res[0] == 19690720:
            print(noun, verb)
        intcode = initialIntcode