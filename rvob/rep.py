# The standard section's names
standard_sections = {".text", ".data", ".bss"}


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

    def get_labels(self):
        """Returns a dictionary of labels mapped to the lines they point to"""

        labd = {}
        lc = 1

        for statement in self.lines:
            for label in statement.labels:
                labd[label] = lc

            lc += 1

        return labd

    def get_sections(self):
        """Returns a list of sections, represented as tuples of (<section name>, <statements list>)"""

        sec_ls = []
        curr_ln, start = 1, 1
        # First line of an assembler source is the first section's header
        curr_sec = self.lines[0].args[0] if self.lines[0].id.__eq__(".section") else self.lines[0].id

        for statement in self.lines[1:]:
            if (type(statement) is Directive) and \
                    (standard_sections.__contains__(statement.id) or statement.id.__eq__(".section")):
                sec_ls.append((curr_sec, self.lines[start:curr_ln]))
                start = curr_ln + 1
                # Remember to update this argument retrieval statement in case we decide to name arguments
                curr_sec = statement.args[0] if statement.id.__eq__(".section") else statement.id

            curr_ln += 1

        sec_ls.append((curr_sec, self.lines[start:curr_ln]))

        return sec_ls


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
        self.type = i_type
        self.instr_args = dict(instr_args)


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
