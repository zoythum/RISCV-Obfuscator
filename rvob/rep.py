class Source:
    """A parsed assembler source file"""

    def __init__(self, statements=None):
        """
        Instantiates a new assembler source file representation
        :param statements: the statements of which the assembler source is composed
        """

        if statements is None:
            self.lines = []
        else:
            self.lines = list(statements)

    def append(self, new_statements):
        """
        Appends a new set of statements to the end of the source
        :param new_statements: the statements to be appended
        :return: None
        """

        self.lines.extend(new_statements)

    def replace(self, start, end, replacement):
        """
        Replaces a set of statements with the provided ones
        :param start: the line number of the first statement to be replaced
        :param end: the line number of the statement after the last one being replaced
        :param replacement: a list of replacement statements
        :return: None
        """

        self.lines[start:end] = replacement


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


class Directive(Statement):
    """A parsed assembler directive"""

    def __init__(self, dir_id, args=None, labels=None):
        """
        Instantiates a new assembler directive statement
        :param dir_id: the directives name
        :param args: a optional list of arguments for the directive
        :param labels: an optional list of labels to mark the directive with
        """

        super().__init__(labels)
        self.id = dir_id

        if args is None:
            self.args = []
        else:
            self.args = list(args)


class Instruction(Statement):
    """A parsed assembly instruction"""

    # TODO refactor this constructor, since its arguments list is too long
    def __init__(self, op_code, i_type, rd=None, rs1=None, rs2=None, immediate=None, labels=None):
        """
        Instantiates a new instruction statement
        :param op_code: the opcode for the new instruction
        :param i_type: the instruction's type
        :param rd: the destination register of the instruction, if any
        :param rs1: the first source register of the instruction, if any
        :param rs2: the last source register of the instruction, if any
        :param immediate: the immediate argument (symbolic or literal) value of the instruction, if any
        :param labels: an optional list of labels to mark the instruction with
        """
        super().__init__(labels)
        self.op_code = op_code
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.immediate = immediate
        self.type = i_type
