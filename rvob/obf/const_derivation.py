from enum import Enum, auto
from typing import Tuple, List, Optional, NamedTuple, Union
from secrets import randbits
from random import seed, choices, sample, randrange
from BitVector import BitVector

from rep.base import Instruction
from structures import Register


class Opcodes(Enum):
    pass


class OtherOps(Opcodes):
    LI = auto()
    SLLI = auto()
    SRLI = auto()


class ALOps(Opcodes):
    ADD = auto()
    ADDI = auto()
    SUB = auto()
    SUBI = auto()
    AND = auto()
    ANDI = auto()
    OR = auto()
    ORI = auto()
    XOR = auto()
    XORI = auto()


class Direction(Enum):
    FROM_MEM = auto()
    TO_MEM = auto()


class ObjectSize(Enum):
    BYTE = 8
    HALF = 16
    WORD = 32


class MemOps(Opcodes):
    LW = (Direction.FROM_MEM, ObjectSize.WORD)
    LH = (Direction.FROM_MEM, ObjectSize.HALF)
    LHU = (Direction.FROM_MEM, ObjectSize.HALF)
    LB = (Direction.FROM_MEM, ObjectSize.BYTE)
    LBU = (Direction.FROM_MEM, ObjectSize.BYTE)
    SW = (Direction.TO_MEM, ObjectSize.WORD)
    SH = (Direction.TO_MEM, ObjectSize.HALF)
    SB = (Direction.TO_MEM, ObjectSize.BYTE)

    def __init__(self, direction: Direction, object_size: ObjectSize):
        self.direction = direction
        self.object_size = object_size


class Promise(NamedTuple):
    op: Opcodes
    rd: Union[int, Register]
    rs1: Optional[Union[int, Register]]
    rs2: Optional[Union[int, Register]]
    const: Optional[Instruction.ImmediateConstant]


class Goal(NamedTuple):
    reg: Union[int, Register]
    const: Instruction.ImmediateConstant


class Derivation(NamedTuple):
    chain: List[Promise]
    remainder: Goal


def mem_primer(target: Instruction) -> Derivation:
    # Generate an equivalent instruction sequence as a memory op with no offset and an already incremented base
    # 0: new address base
    # 1: register from where the offset is to be loaded
    starting_sequence = [
        Promise(MemOps[target.opcode.upper()], target.r1, 0, None, Instruction.ImmediateConstant(12, None, 0)),
        Promise(ALOps.ADD, 0, target.r2, 1, None)
    ]

    # Prime the derivation with the starting sequence and the correct promise
    return Derivation(starting_sequence, Goal(1, target.immediate))


def imm_primer(target: Instruction) -> Derivation:
    # Substitute the given instruction with its R-format counterpart and initialize the goal with its immediate value
    return Derivation([Promise(ALOps[target.opcode[:-1].upper()], target.r1, target.r2, 0, None)],
                      Goal(0, target.immediate))


def shifter_obf(goal: Goal) -> Tuple[Promise, Goal]:
    def _count_leading_zeros(constant: BitVector):
        leading_zeroes = 0
        while constant[0] == 0:
            leading_zeroes += 1
            constant <<= 1

        return leading_zeroes

    def _count_trailing_zeroes(constant: BitVector):
        trailing_zeroes = 0
        while constant[-1] == 0:
            trailing_zeroes += 1
            constant >>= 1

        return trailing_zeroes

    lead = _count_leading_zeros(goal.const.value)
    trail = _count_trailing_zeroes(goal.const.value)

    if lead > trail:
        shift = lead
        new_val = goal.const.value << lead
        instruction = OtherOps.SRLI
    else:
        shift = trail
        new_val = goal.const.value >> trail
        instruction = OtherOps.SLLI

    return (Promise(instruction, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, shift)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(new_val.size, None, new_val.int_val())))


def logic_ori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    noise = randbits(goal.const.size)
    immediate = goal.const.int_val
    # (A and !B) or (A and B) equals A
    return (Promise(ALOps.ORI, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, immediate & ~noise)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(goal.const.size, None, immediate & noise)))


def logic_andi_obf(goal: Goal) -> Tuple[Promise, Goal]:
    noise = randbits(goal.const.size)
    immediate = goal.const.int_val
    # (A or !B) and (A or B) equals A
    return (Promise(ALOps.ANDI, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, immediate | ~noise)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(goal.const.size, None, immediate | noise)))


def logic_xori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    noise = randbits(goal.const.size)
    immediate = goal.const.int_val
    # (A xor B) xor B equals A
    return (Promise(ALOps.XORI, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, immediate ^ noise)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(goal.const.size, None, noise)))


def terminator(goal: Goal) -> Promise:
    # Simply load the goal's value through a load immediate instruction
    return Promise(OtherOps.LI, goal.reg, None, None,
                   Instruction.ImmediateConstant(goal.const.size, None, goal.const.int_val))


primers = {
    "addi": imm_primer,
    "subi": imm_primer,
    "andi": imm_primer,
    "ori": imm_primer,
    "xori": imm_primer,
    "lw": mem_primer,
    "lh": mem_primer,
    "lhu": mem_primer,
    "lb": mem_primer,
    "lbu": mem_primer,
    "sw": mem_primer,
    "sh": mem_primer,
    "sb": mem_primer
}

logic_obfuscators = [logic_andi_obf, logic_ori_obf, logic_xori_obf]


def generate_derivation_chain(instruction: Instruction, max_shifts: int, max_logical: int, min_length: int = 0)\
        -> List[Promise]:
    seed()
    # Prime the obfuscation chain
    oc = primers[instruction.opcode](instruction)

    # Build the obfuscators' pool
    obfuscators = choices(population=logic_obfuscators, k=max_logical) + ([shifter_obf] * max_shifts)
    obfuscators = sample(population=obfuscators, k=randrange(min_length, max_shifts + max_logical))

    # Grow the chain
    for obf in obfuscators:
        new_derivation_step, new_goal = obf(oc.remainder)
        oc = Derivation(oc.chain + [new_derivation_step], new_goal)

    # Terminate chain and return it
    return oc.chain + [terminator(oc.remainder)]
