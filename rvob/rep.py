from collections import namedtuple

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
        lc = 0

        for statement in self.lines:
            for label in statement.labels:
                labd[label] = lc

            lc += 1

        return labd

    def get_sections(self):
        """
        Returns a list of sections, represented as tuples of (<section name>, <start>, <end>, <statements list>).

        Keep in mind that <start> and <end> represent the index of the first line of the section and the position
        after the last line, respectively, much like as in the list slicing convention.
        """

        # Create a named tuple class for storing the section's information
        section_nt = namedtuple("Section", 'name start end statements')

        sec_ls = []
        curr_ln, start = 1, 1
        # The first part of an assembler source contains options for GAS, so we ignore it
        # TODO  maybe define this as a special fake section?
        curr_sec = None

        for statement in self.lines[1:]:
            if (type(statement) is Directive) and \
                    (standard_sections.__contains__(statement.name) or ".section" == statement.name):
                # If not the first section, conclude the previous one and add it to the returned list
                if curr_sec is not None:
                    sec_ls.append(section_nt(curr_sec, start, curr_ln, self.lines[start:curr_ln]))

                start = curr_ln + 1
                # Remember to update this argument retrieval statement in case we decide to name arguments
                curr_sec = statement.args["args"][0] if ".section" == statement.name else statement.name

            curr_ln += 1

        sec_ls.append(section_nt(curr_sec, start, curr_ln, self.lines[start:curr_ln]))

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
        self.name = name

        if kwargs is None:
            self.args = {}
        else:
            self.args = dict(kwargs)

    def __repr__(self):
        return repr(self.name) + ", " + repr(self.labels) + ", " + repr(self.args)

    def __str__(self):
        return str(self.name) + " " + str(self.args)


class Instruction(Statement):
    """A parsed assembly instruction"""

    def __init__(self, opcode, family, labels=None, **instr_args):
        """
        Instantiates a new instruction statement
        :param op_code: the opcode for the new instruction
        :param i_type: the instruction's type
        :param instr_args: the instruction's arguments
        :param labels: an optional list of labels to mark the instruction with
        """
        super().__init__(labels)
        self.opcode = opcode
        self.family = family
        self.instr_args = dict(instr_args)

    def __repr__(self):
        return repr(self.opcode) + ", " + repr(self.family) + ", " + repr(self.labels) + ", " + repr(self.instr_args)

    def __str__(self):
        return str(self.opcode) + " " + str(self.instr_args)


# Classes catalogue
classes = {
    "directive": Directive,
    "instruction": Instruction
}


def load_src(descriptions: list) -> Source:
    """Loads a list of dictionary descriptions of parsed assembler statements
    :param descriptions: a list of dictionaries, describing a single assembler statement each
    :return: a new source object
    """

    labs = []
    statements = []
    for d in descriptions:
        if "label" == d["role"]:
            labs.append(d["name"])
        else:
            constructor = classes[d["role"]]
            # We don't need a role inside our structure because the type of structure already defines the role
            del d["role"]
            statements.append(constructor(labels=labs, **d))
            labs = []

    return Source(statements)
