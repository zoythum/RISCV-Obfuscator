def uFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.immediate)+"\n"


def iFamily(instr):
    return "\t" + str(instr.opcode) + "\t" + str(instr.r1) + "," + str(instr.r2) + "," + str(instr.immediate) + "\n"


def sFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.immediate)+"("+str(instr.r2)+")\n"


def rFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.r2)+","+str(instr.r3)+"\n"


def jFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.immediate)+"\n"


def jrFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+"\n"


def bFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.r2)+","+str(instr.immediate)+"\n"


def alFamily(instr):
    return "\t" + str(instr.opcode) + "\t" + str(instr.r1) + "," + str(instr.immediate) + "(" + str(instr.r2) + ")\n"


def asFamily(instr):
    return "\t" + str(instr.opcode) + "\t" + str(instr.r1) + "," + str(instr.r2) + "," + str(instr.immediate) + "(" + str(instr.r3) + ")\n"


def sextFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.r2)+"\n"


def _2argFamily(instr):
    if instr.r2 is None:
        return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.immediate)+"\n"
    else:
        return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.r2)+"\n"


def bzFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.immediate)+"\n"


def nopFamily(instr):
    return "\t"+str(instr.opcode)+"\n"


def snezFamily(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.r1)+","+str(instr.r2)+"\n"


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