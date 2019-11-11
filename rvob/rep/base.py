from typing import NamedTuple, Union, Iterator

from BitVector import BitVector

from structures import imm_sizes


class Statement:
    """An assembler source statement"""

    def __init__(self, labels=None):
        """
        Instantiates a new assembler source statement
        :param labels: an optional set of labels to mark the new statement with
        """

        if labels is None:
            self.labels = []
        else:
            self.labels = list(labels)


class Instruction(Statement):
    """A parsed assembly instruction"""

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

        _symbol: Union[str, None]
        _value: Union[BitVector, None]
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
                for f in range(1, size):
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
            value_str = " [" + str(self.int_val) + "]" if self._value is not None else ""
            return ("<literal>" if self._symbol is None else str(self._symbol)) + value_str

    def __init__(self, opcode, family, labels=None, **instr_args):
        """
        Instantiates a new instruction statement.

        :param op_code: the opcode for the new instruction
        :param i_type: the instruction's type
        :param instr_args: the instruction's arguments
        :param labels: an optional list of labels to mark the instruction with
        """
        super().__init__(labels)
        self.opcode = opcode
        self.family = family
        self.instr_args = dict(instr_args)

        if family in imm_sizes:
            if isinstance(instr_args["immediate"], int):
                # Constant as literal value
                self.instr_args["immediate"] = Instruction.ImmediateConstant(value=instr_args["immediate"],
                                                                             size=imm_sizes[family])
            elif isinstance(instr_args["immediate"], str):
                # Constant as symbolic value
                self.instr_args["immediate"] = Instruction.ImmediateConstant(symbol=instr_args["immediate"],
                                                                             size=imm_sizes[family])

    def __repr__(self):
        return repr(self.opcode) + ", " + repr(self.family) + ", " + repr(self.labels) + ", " + repr(self.instr_args)

    def __str__(self):
        return str(self.opcode) + " " + str(self.instr_args)


class Directive(Statement):
    """A parsed assembler directive"""

    def __init__(self, name, labels=None, **kwargs):
        """
        Instantiates a new assembler directive statement
        :param name: the directives name
        :param labels: an optional list of labels to mark the directive with
        :param kwargs: a optional list of arguments for the directive
        """

        super().__init__(labels)
        self.name = name

        if kwargs is None:
            self.args = {}
        else:
            self.args = dict(kwargs)

    def __repr__(self):
        return repr(self.name) + ", " + repr(self.labels) + ", " + repr(self.args)

    def __str__(self):
        return str(self.name) + " " + str(self.args)


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
