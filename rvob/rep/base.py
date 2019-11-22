from typing import NamedTuple, Union, Iterator, Sequence, Optional

from BitVector import BitVector

from rep.instruction_repr import familystr
from structures import Register, imm_sizes


class Statement:
    """An assembler source statement."""

    labels: Sequence[str]

    def __init__(self, labels: Optional[Sequence[str]] = None):
        """
        Instantiates a new assembler source statement.

        :param labels: an optional set of labels to mark the new statement with
        """

        if labels is None:
            self.labels = []
        else:
            self.labels = list(labels)

    def __str__(self):
        return "".join(lab+":\n" for lab in self.labels)


class Instruction(Statement):
    """A parsed assembly instruction."""

    class ImmediateConstant:
        """
        An immediate constant.

        This class represents some sort of constant used as an immediate value by an instruction.
        Such constant can be a literal value or a symbolic one.
        Immediate formats can differ in size, so a size must be specified at creation time for faithful representation
        and correct manipulation of the binary value.

        :var symbol: the symbolic identifier of the constant, if any
        :var value: the binary representation of the value, if assigned
        :var int_val: the integer representation of the value, if assigned
        :var size: the size in bits of the containing immediate field
        """

        _symbol: Optional[str]
        _value: Optional[BitVector]
        _size: int

        def __init__(self, size, symbol: str = None, value: int = None):
            """
            Instantiate an immediate constant of the specified size and value, identified by a symbol.

            :param size: the size in bits of the constant
            :param symbol: the symbol identifying the constant, if any
            :param value: the integer value of the constant, if any
            :raise ValueError: when both symbol and value are left unspecified
            """

            if symbol is None and value is None:
                raise ValueError("Constant must be symbolic or have a value")

            self._size = size
            self._symbol = symbol

            if value is not None:

                # Prepare the mask for cutting the supplied value's bit representation to the specified size
                mask = 0
                for f in range(0, size):
                    mask += 2 ** f

                value = value & mask
                self._value = BitVector(intVal=value, size=size)

                # Sizes must be coherent
                assert self._size == len(self._value)
            else:
                self._value = None

        @property
        def symbol(self) -> str:
            return self._symbol

        @property
        def value(self) -> BitVector:
            return self._value.deep_copy()

        @property
        def int_val(self) -> int:
            # Return the constant's integer representation, preserving its sign through an overly complicated procedure
            return -((~self._value).int_val() + 1) if self._value[0] == 1 else self._value.int_val()

        @property
        def size(self):
            return self._size

        def __repr__(self):
            return "Instruction.ImmediateConstant(size=" + repr(self._size) + ", symbol=" + repr(self._symbol) + \
                   ", value=" + repr(None if self._value is None else self.int_val) + ")"

        def __str__(self):
            return str(self.int_val) if self._symbol is None else self.symbol

    opcode: str
    family: str
    r1: Optional[Register]
    r2: Optional[Register]
    r3: Optional[Register]
    immediate: Optional[ImmediateConstant]

    def __init__(self, opcode: str, family: str, labels: Sequence[str] = None, r1: Union[str, Register] = None,
                 r2: Union[str, Register] = None, r3: Union[str, Register] = None,
                 immediate: Union[str, int, ImmediateConstant] = None):
        """
        Instantiates a new instruction statement.

        :param opcode: the opcode of the new instruction
        :param family: the instruction's format
        :param labels: an optional list of labels to mark the instruction with
        :param r1: the first register parameter, if any
        :param r2: the second register parameter, if any
        :param r3: the third register parameter, if any
        :param immediate: the immediate constant passed to the function, if any
        """

        # Clean register arguments from the 'unused' keyword and raise an exception if a 'reg_err' is found
        if r1 == "reg_err" or r2 == "reg_err" or r3 == "reg_err":
            raise ValueError("Received the output of a failed parsing pass")

        r1 = r1 if r1 != "unused" else None
        r2 = r2 if r2 != "unused" else None
        r3 = r3 if r3 != "unused" else None

        super().__init__(labels)
        self.opcode = opcode
        self.family = family
        self.r1 = Register[r1.upper()] if type(r1) is str else r1
        self.r2 = Register[r2.upper()] if type(r2) is str else r2
        self.r3 = Register[r3.upper()] if type(r3) is str else r3

        if family in imm_sizes:
            if isinstance(immediate, int):
                # Constant as literal value
                self.immediate = Instruction.ImmediateConstant(value=immediate,
                                                               size=imm_sizes[family])
            elif isinstance(immediate, str):
                # Constant as symbolic value
                self.immediate = Instruction.ImmediateConstant(symbol=immediate,
                                                               size=imm_sizes[family])
            else:
                # Maybe an ImmediateConstant itself
                self.immediate = immediate
        else:
            self.immediate = None

    def __repr__(self):
        return "Instruction(" + repr(self.opcode) + ", " + repr(self.family) + ", " + repr(self.labels) + ", " + \
               repr(self.r1) + ", " + repr(self.r2) + ", " + repr(self.r3) + ", " + repr(self.immediate) + ")"

    def __str__(self):
        return super().__str__()+familystr[self.family](self)


class Directive(Statement):
    """A parsed assembler directive."""

    name: str
    args: Sequence[str]

    def __init__(self, name: str, labels: Optional[Sequence[str]] = None, args: Optional[Sequence[str]] = None):
        """
        Instantiates a new assembler directive statement.

        :param name: the directive's name
        :param labels: an optional list of labels to mark the directive with
        :param args: an optional sequence of arguments for the directive
        """

        super().__init__(labels)
        self.name = name

        if args is None:
            self.args = []
        else:
            self.args = list(args)

    def __repr__(self):
        return "Directive(" + repr(self.name) + ", " + repr(self.labels) + ", " + repr(self.args) + ")"

    def __str__(self):
        # TODO investigate correctness of this string representation
        return super().__str__() + "\t" + str(self.name) + "\t" + ", ".join(self.args) + "\n"


class ASMLine(NamedTuple):
    """An assembler source line."""

    number: int
    statement: Statement


def to_line_iterator(statement_iterator: Iterator[Statement], starting_line: int = 0) -> Iterator[ASMLine]:
    """
    Wrap an iterator over statements to make it an iterator over assembly lines.

    For every statement returned by the wrapped iterator, an ASMLine object is made out of it, incrementing the line
    number starting from the provided one, or 0 by default.

    :param statement_iterator: the iterator to be wrapped
    :param starting_line: the line number from which line numbering will start
    :return: an iterator over ASM lines
    """

    current_line = starting_line
    for statement in statement_iterator:
        yield ASMLine(current_line, statement)
        current_line += 1
