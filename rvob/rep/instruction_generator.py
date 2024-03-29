from random import choice, getrandbits
from rep.base import Instruction


def addi_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("addi", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def slti_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("slti", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def sltiu_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sltiu", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def xori_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("xori", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def ori_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("ori", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def andi_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("andi", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def slli_instr(free_regs: list, used_reg: list) -> Instruction:
    # generates a 5-bit immediate, only these are meaningful for the instruction

    return Instruction("slli", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(5))


def srli_instr(free_regs: list, used_reg: list) -> Instruction:
    # generates a 5-bit immediate, only these are meaningful for the instruction

    return Instruction("srli", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(5))


def srai_instr(free_regs: list, used_reg: list) -> Instruction:
    # generates a 5-bit immediate, only these are meaningful for the instruction

    return Instruction("srai", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(5))


def addiw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("addiw", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(12))


def slliw_instr(free_regs: list, used_reg: list) -> Instruction:
    # generates a 5-bit immediate, only these are meaningful for the instruction

    return Instruction("slliw", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(5))


def srliw_instr(free_regs: list, used_reg: list) -> Instruction:
    # generates a 5-bit immediate, only these are meaningful for the instruction

    return Instruction("srliw", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(5))


def sraiw_instr(free_regs: list, used_reg: list) -> Instruction:
    # generates a 5-bit immediate, only these are meaningful for the instruction

    return Instruction("sraiw", "i", r1=choice(free_regs), r2=choice(used_reg), immediate=getrandbits(5))


def mv_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("mv", "_2arg", r1=choice(free_regs), r2=choice(used_reg))


def add_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("add", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def sub_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sub", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def sll_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sll", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def slt_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("slt", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def sltu_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sltu", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def xor_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("xor", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def srl_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("srl", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def sra_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sra", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def or_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("or", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def and_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("and", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def addw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("addw", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def subw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("subw", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def sllw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sllw", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def srlw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("srlw", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def sraw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("sraw", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def mul_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("mul", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def mulh_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("mulh", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def mulhsu_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("mulhsu", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def mulhu_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("mulhu", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


def mulw_instr(free_regs: list, used_reg: list) -> Instruction:
    return Instruction("mulw", "r", r1=choice(free_regs), r2=choice(used_reg), r3=choice(used_reg))


garbage_inst = {"addi": addi_instr,
                "slti": slti_instr,
                "sltiu": sltiu_instr,
                "xori": xori_instr,
                "ori": ori_instr,
                "andi": andi_instr,
                "slli": slli_instr,
                "srli": srli_instr,
                "srai": srai_instr,
                "addiw": addiw_instr,
                "slliw": slliw_instr,
                "srliw": srliw_instr,
                "mv": mv_instr,
                "sraiw": sraiw_instr,
                "add": add_instr,
                "sub": sub_instr,
                "sll": sll_instr,
                "slt": slt_instr,
                "sltu": sltu_instr,
                "xor": xor_instr,
                "srl": srl_instr,
                "sra": sra_instr,
                "or": or_instr,
                "and": and_instr,
                "addw": addw_instr,
                "subw": subw_instr,
                "sllw": sllw_instr,
                "srlw": srlw_instr,
                "sraw": sraw_instr,
                "mul": mul_instr,
                "mulh": mulh_instr,
                "mulhsu": mulhsu_instr,
                "mulhu": mulhu_instr,
                "mulw": mulw_instr}
