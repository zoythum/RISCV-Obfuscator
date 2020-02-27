
def u_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)+"\n"


def i_family(instr):
    return "\t" + str(instr.opcode) + "\t" + instr.r1.name.lower() + "," + instr.r2.name.lower() \
           + "," + str(instr.immediate) + "\n"


def s_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)\
           + "(" + instr.r2.name.lower()+")\n"


def r_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","\
           +instr.r2.name.lower()+","+instr.r3.name.lower()+"\n"


def j_family(instr):
    return "\t"+str(instr.opcode)+"\t"+str(instr.immediate)+"\n"


def jr_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+"\n"


def b_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+","\
           + str(instr.immediate)+"\n"


def al_family(instr):
    return "\t" + str(instr.opcode) + "\t" + instr.r1.name.lower() + "," + str(instr.immediate) + "(" \
           + instr.r2.name.lower() + ")\n"


def as_family(instr):
    return "\t" + str(instr.opcode) + "\t" + instr.r1.name.lower() + "," + instr.r2.name.lower() \
           + "," + str(instr.immediate) + "(" + instr.r3.name.lower() + ")\n"


def sext_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+"\n"


def _2arg_family(instr):
    if instr.r2 is None:
        return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)+"\n"
    else:
        return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+"\n"


def bz_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+str(instr.immediate)+"\n"


def nop_family(instr):
    return "\t"+str(instr.opcode)+"\n"


def snez_family(instr):
    return "\t"+str(instr.opcode)+"\t"+instr.r1.name.lower()+","+instr.r2.name.lower()+"\n"


familystr = {"u": u_family,
             "i": i_family,
             "s": s_family,
             "r": r_family,
             "j": j_family,
             "jr": jr_family,
             "b": b_family,
             "al": al_family,
             "as": as_family,
             "sext": sext_family,
             "_2arg": _2arg_family,
             "bz": bz_family,
             "nop": nop_family,
             "snez": snez_family}
