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

    def __init__(self, name, labels=None, **kwargs):
        """
        Instantiates a new assembler directive statement
        :param name: the directives name
        :param labels: an optional list of labels to mark the directive with
        :param kwargs: a optional list of arguments for the directive
        """

        super().__init__(labels)
        self.id = name

        if kwargs is None:
            self.args = {}
        else:
            self.args = dict(kwargs)


class Instruction(Statement):
    """A parsed assembly instruction"""

    def __init__(self, op_code, i_type, labels=None, **instr_args):
        """
        Instantiates a new instruction statement
        :param op_code: the opcode for the new instruction
        :param i_type: the instruction's type
        :param instr_args: the instruction's arguments
        :param labels: an optional list of labels to mark the instruction with
        """
        super().__init__(labels)
        self.op_code = op_code
        self.instr_args = instr_args
        self.type = i_type


# Constructors catalogue
constructors = {
    "directive": Directive.__init__,
    "instruction": Instruction.__init__
}


def load_src(descriptions: list) -> Source:
    """Loads a list of dictionary descriptions of parsed assembler statements
    :param descriptions: a list of dictionaries, describing a single assembler statement each
    :return: a new source object
    """

    labs = []
    statements = []
    for d in descriptions:
        if "label".__eq__(d["type"]):
            labs.append(d["name"])
        else:
            constructor = constructors[d["type"]]
            del d["type"]
            statements.append(constructor(labels=labs, **d))
            labs = []

    return Source(statements)
