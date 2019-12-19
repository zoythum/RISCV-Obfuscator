from enum import Enum, auto
from typing import Tuple, List, Optional, NamedTuple, Union

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


class MemOps(Opcodes):
    class Direction(Enum):
        FROM_MEM = auto()
        TO_MEM = auto()

    class ObjectSize(Enum):
        BYTE = 8
        HALF = 16
        WORD = 32

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

    # Prime the derivation with the starting sequence anf the correct promise
    return Derivation(starting_sequence, Goal(1, target.immediate.value))


def imm_primer(target: Instruction) -> Derivation:
    pass


def shifter_obf(goal: Goal) -> Tuple[Promise, Goal]:
    pass


def logic_ori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    pass


def logic_andi_obf(goal: Goal) -> Tuple[Promise, Goal]:
    pass


def logic_xori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    pass


def terminator(goal: Goal) -> Promise:
    pass


primers = {
    Opcodes.ADD: imm_primer,
    Opcodes.SUB: imm_primer,
    Opcodes.AND: imm_primer,
    Opcodes.OR: imm_primer,
    Opcodes.XOR: imm_primer,
    Opcodes.LW: mem_primer,
    Opcodes.LH: mem_primer,
    Opcodes.LHU: mem_primer,
    Opcodes.LB: mem_primer,
    Opcodes.LBU: mem_primer,
    Opcodes.SW: mem_primer,
    Opcodes.SH: mem_primer,
    Opcodes.SB: mem_primer
}
