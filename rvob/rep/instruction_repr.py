
from rvob.structures import Register


def uFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)+"\n"


def iFamily(instr):
    return "\t" + str(instr.opcode) + "\t" + instr.r1.name.lower() + "," + instr.r2.name.lower() \
           + "," + str(instr.immediate) + "\n"


def sFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)\
           + "(" + instr.r2.name.lower()+")\n"


def rFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","\
           +instr.r2.name.lower()+","+instr.r3.name.lower()+"\n"


def jFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.immediate)+"\n"


def jrFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+"\n"


def bFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+","\
           + str(instr.immediate)+"\n"


def alFamily(instr):
    return "\t" + str(instr.opcode) + "\t" + instr.r1.name.lower() + "," + str(instr.immediate) + "(" \
           + instr.r2.name.lower() + ")\n"


def asFamily(instr):
    return "\t" + str(instr.opcode) + "\t" + instr.r1.name.lower() + "," + instr.r2.name.lower() \
           + "," + str(instr.immediate) + "(" + instr.r3.name.lower() + ")\n"


def sextFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+"\n"


def _2argFamily(instr):
    if instr.r2 is None:
        return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)+"\n"
    else:
        return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+"\n"


def bzFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)+"\n"


def nopFamily(instr):
    return "\t"+str(instr.opcode)+"\n"


def snezFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+"\n"


familystr = {"u": uFamily,
             "i": iFamily,
             "s": sFamily,
             "r": rFamily,
             "j": jFamily,
             "jr": jrFamily,
             "b": bFamily,
             "al": alFamily,
             "as": asFamily,
             "sext": sextFamily,
             "_2arg": _2argFamily,
             "bz": bzFamily,
             "nop": nopFamily,
             "snez": snezFamily}