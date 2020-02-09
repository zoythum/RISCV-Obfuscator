from enum import Enum, auto
from typing import Tuple, List, Optional, NamedTuple, Union
from secrets import randbits

from rep.base import Instruction
from structures import Register


class Opcodes(Enum):
    pass


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
    rs1: Union[int, Register]
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
    return Derivation(starting_sequence, Goal(1, target.immediate.value))


def imm_primer(target: Instruction) -> Derivation:
    # Substitute the given instruction with its R-format counterpart and initialize the goal with its immediate value
    return Derivation([Promise(ALOps[target.opcode[:-1]], target.r1, target.r2, 0, None)],
                      Goal(0, target.immediate.value))


def shifter_obf(goal: Goal) -> Tuple[Promise, Goal]:
    pass


def logic_ori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    noise = randbits(goal.const.size)
    # (A and !B) or (A and B) equals A
    return (Promise(Opcodes.ORI, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, goal.const.int_val & ~noise)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(goal.const.size, None, goal.const.int_val & noise)))


def logic_andi_obf(goal: Goal) -> Tuple[Promise, Goal]:
    noise = randbits(goal.const.size)
    # (A or !B) and (A or B) equals A
    return (Promise(Opcodes.ANDI, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, goal.const.int_val | ~noise)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(goal.const.size, None, goal.const.int_val | noise)))


def logic_xori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    noise = randbits(goal.const.size)
    # (A xor B) xor B equals A
    return (Promise(Opcodes.XORI, goal.reg, goal.reg + 1, None,
                    Instruction.ImmediateConstant(goal.const.size, None, goal.const.int_val ^ noise)),
            Goal(goal.reg + 1, Instruction.ImmediateConstant(goal.const.size, None, noise)))


def terminator(goal: Goal) -> Promise:
    pass


primers = {
    ALOps.ADD: imm_primer,
    ALOps.SUB: imm_primer,
    ALOps.AND: imm_primer,
    ALOps.OR: imm_primer,
    ALOps.XOR: imm_primer,
    MemOps.LW: mem_primer,
    MemOps.LH: mem_primer,
    MemOps.LHU: mem_primer,
    MemOps.LB: mem_primer,
    MemOps.LBU: mem_primer,
    MemOps.SW: mem_primer,
    MemOps.SH: mem_primer,
    MemOps.SB: mem_primer
}
