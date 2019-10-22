from __future__ import annotations

from abc import ABC, abstractmethod
from collections import namedtuple, MutableSequence, Hashable
from typing import List, Iterator, MutableMapping, ClassVar, NamedTuple, Sequence, Union
from weakref import WeakKeyDictionary

# The standard section's names
standard_sections = {".text", ".data", ".bss"}


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


class CodeFragment(ABC, MutableSequence, Hashable):
    """
    A fragment of assembly code.

    A code fragment is an iterable container of statements which represents a (eventually improper) portion (or
    excision) of an assembler source.
    Objects of this class support some of the access and modification methods one can expect from a mutable list.
    This is an abstract class meant to be extended by concrete implementations; the constructor and the slice() method
    only have a minimal implementation that checks for consistency.
    """

    # noinspection PyStatementEffect
    def __init__(self, src: Sequence[Statement], begin: int = 0, end: int = 0, offset: int = 0) -> None:
        """
        Generates a new code fragment object from a sequence of assembly statements.

        The new fragment will represent lines from number begin to end excluded, taking statements from the list
        starting from the specified offset.
        This minimal implementation checks if the size of the excision fits in the provided source list, expecting the
        subclasses' constructors to do the rest according to their inner workings.

        :param src: the list of statement from which the fragment's contents will be excised
        :param begin: line number of the first line contained in the new fragment
        :param end: line number of the first line following the last contained in the new fragment
        :param offset: offset of the new code fragment inside the origin sequence
        :raises ValueError: when the fragment size would not fit inside the origin sequence
        """

        # Ugly, but it works even for sequences not starting from 0 (e.g. code fragments)
        try:
            src[offset]
            src[offset + end - begin - 1]
        except IndexError:
            raise ValueError("Fragment out of origin range")

    @abstractmethod
    def get_begin(self) -> int:
        """
        Returns the line number of the first line contained in this fragment.

        :return: the first line's line number
        """

        pass

    @abstractmethod
    def get_end(self) -> int:
        """
        Returns the line number of the line after the last one contained in this fragment.

        :return: the line number of the first line that follows the block
        """

        pass

    @abstractmethod
    def get_offset(self) -> int:
        """
        Returns the offset of this fragment with respect to the original statements list.

        :return: the offset of this fragment wrt the start of the original source
        """

        pass

    # noinspection PyTypeChecker
    @abstractmethod
    def slice(self, start: int, end: int) -> CodeFragment:
        """
        Stub for a slicing function.

        This abstract implementation verifies that the slice is in fact part of the original fragment.

        :param start: the starting line of the new fragment
        :param end: the end line of the new fragment
        :raises ValueError: when the specified interval doesn't fit inside the existing fragment
        """

        if start < self.get_begin() or end > self.get_end():
            raise ValueError("Slice out of fragment range")

    @abstractmethod
    def append(self, statement: Statement) -> None:
        """
        Appends the provided statement to the fragment.

        :param statement: the statement to be appended
        """

        pass

    @abstractmethod
    def extend(self, statements: List[Statement]) -> None:
        """
        Extends this fragment with the statements contained in the supplied list.

        :param statements: a list of statements to be appended
        """

        pass

    @abstractmethod
    def insert(self, line_number: int, statement: Statement) -> None:
        """
        Inserts a new statement in this fragment.

        :param line_number: the position (i.e. line number) at which the new statement will reside
        :param statement: the statement to be inserted
        :raises IndexError
        """

        pass

    @abstractmethod
    def pop(self, line_number: int = -1) -> Statement:
        """
        Pops a statement at a given position.

        :param line_number: the position (i.e. line number) of the statement to be popped
        :raises IndexError
        """

        pass

    @abstractmethod
    def copy(self) -> CodeFragment:
        """
        Stub for a copying method.

        Subclasses are expected to deal with how data and statements are copied.

        :return: a copy of this fragment
        """

        pass

    @abstractmethod
    def clear(self) -> None:
        """Empties this fragment."""

        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Statement]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, line_number: Union[int, slice]) -> Union[Statement, CodeFragment]:
        pass

    @abstractmethod
    def __setitem__(self, line_number: Union[int, slice], statement: Union[Statement, Sequence[Statement]]) -> None:
        pass

    @abstractmethod
    def __delitem__(self, line_number: Union[int, slice]) -> None:
        pass


class FragmentCopy(CodeFragment):
    """
    A code fragment obtained by copy.

    This implementation of CodeFragment operates with a copied slice of the source sequence of statements, therefore
    keeping all modifications away from the original.

    :var begin: the line number of the first line contained in this fragment
    :var end: the line number of the line following the last one contained in this fragment
    :var offset: the offset of this fragment wrt the start of the original source sequence
    """

    def __init__(self, src: Sequence[Statement], begin: int = 0, end: int = 0, offset: int = 0) -> None:
        """
        Generates a new copy-fragment object from a sequence of assembly statements.

        :param src: the list of statement from which the fragment's contents will be excised
        :param begin: line number of the first line contained in the new fragment
        :param end: line number of the first line following the last contained in the new fragment
        :param offset: offset of the new code fragment inside the origin sequence
        :raises ValueError: when the fragment size would not fit inside the origin sequence
        """

        # Delegate consistency checks
        super().__init__(src, begin, end, offset)

        self.begin: int = begin
        self.end: int = end
        self.offset: int = offset
        self.__lines__: List[Statement] = list(src[offset:offset + end - begin])

    # Utility method for calculating a line's position inside the origin list, given its line number
    def __line_to_index__(self, line_number: int) -> int:
        index = line_number - self.begin

        # Negative line numbers have no meaning
        if index < 0:
            raise IndexError("Index out of range")

        return index

    def get_begin(self) -> int:
        return self.begin

    def get_end(self) -> int:
        return self.end

    def get_offset(self) -> int:
        return self.offset

    def slice(self, start: int, end: int) -> FragmentCopy:
        """
        Creates a new fragment by slicing.

        The newly created fragment is an independent shallow-copied slice of the current one, representing a contiguous
        subset of its statements.
        These objects can be accessed by slicing only if the ranges fall within the range of contained line numbers.

        :param start: the starting line of the new fragment
        :param end: the end line of the new fragment
        :return: a FragmentCopy representing a slice of the contained statements
        :raises ValueError: when the specified interval doesn't fit inside the existing fragment
        """

        # Delegate consistency checks
        super().slice(start, end)
        return FragmentCopy(self.__lines__, start, end, start - self.begin)

    def append(self, statement: Statement) -> None:
        self.__lines__.append(statement)
        self.end += 1

    def extend(self, statements: List[Statement]) -> None:
        self.__lines__.extend(statements)
        self.end += len(statements)

    def insert(self, line_number: int, statement: Statement) -> None:
        self.__lines__.insert(self.__line_to_index__(line_number), statement)
        self.end += 1

    def pop(self, line_number: int = -1) -> Statement:
        popped = self.__lines__.pop(self.__line_to_index__(line_number))
        self.end -= 1
        return popped

    def copy(self) -> FragmentCopy:
        """
        Makes a shallow copy of this fragment.

        :return: a shallow copy of this fragment
        """

        return FragmentCopy(self.__lines__, self.begin, self.end, self.offset)

    def clear(self) -> None:
        self.__lines__.clear()
        self.end = self.begin

    def __iter__(self) -> Iterator[Statement]:
        return self.__lines__.__iter__()

    def __len__(self) -> int:
        return len(self.__lines__)

    def __getitem__(self, line_number: Union[int, slice]) -> Union[Statement, FragmentCopy]:
        if type(line_number) is int:
            return self.__lines__[self.__line_to_index__(line_number)]
        elif type(line_number) is slice:
            # We return a FragmentCopy representing the slice, but notice how the offset info gets lost
            return FragmentCopy(self.__lines__[self.__line_to_index__(line_number.start):
                                               self.__line_to_index__(line_number.stop):
                                               line_number.step],
                                line_number.start,
                                line_number.stop,
                                0)
        else:
            raise TypeError("Integer index or slice expected")

    def __setitem__(self, line_number: Union[int, slice], statement: Union[Statement, Sequence[Statement]]) -> None:
        if type(line_number) is int:
            self.__lines__[self.__line_to_index__(line_number)] = statement
        elif type(line_number) is slice:
            self.__lines__[self.__line_to_index__(line_number.start):
                           self.__line_to_index__(line_number.stop):
                           line_number.step] = statement

            if len(statement) == 0:
                # A funky deletion just took place, so we must treat it accordingly
                self.end -= line_number.stop - line_number.start
        else:
            raise TypeError("Integer index/statement or slice/list expected")

    def __delitem__(self, line_number: Union[int, slice]) -> None:
        if type(line_number) is int:
            del self.__lines__[self.__line_to_index__(line_number)]
            self.end -= 1
        elif type(line_number) is slice:
            del self.__lines__[self.__line_to_index__(line_number.start):
                               self.__line_to_index__(line_number.stop):
                               line_number.step]

            # Decrease the list's size according to the number of elements that got deleted
            self.end -= len(range(line_number.start,
                                  line_number.stop,
                                  1 if line_number.step is None else line_number.step))
        else:
            raise TypeError("Integer index/statement or slice/list expected")

    def __hash__(self) -> int:
        # The embedded list's lifecycle is tightly coupled with the fragment's one, so this should suffice
        return hash((id(self), id(self.__lines__)))


class FragmentView(CodeFragment):
    """
    A code fragment-view of an assembler source snippet.

    This kind of code fragment defines a modifiable view of the assembly code contained in another code fragment.
    Multiple views of the same or different parts of an assembler source can be instantiated, and a shared data
    structure ensures that any update performed through the objects of this class is correctly reflected in the overall
    code layout presented through these views.
    Be aware that any structural modification performed directly on the origin leaves the whole view system in an
    inconsistent state. To regain consistency, discard the corrupted views and recreate them.
    """

    # Named tuple used for containing views' metadata
    class FragmentReferenceFrame(NamedTuple):
        begin: int
        end: int
        offset: int

    # Declare and allocate the shared catalogue of source fragments
    __sources_catalogue__: ClassVar[
        MutableMapping[
            CodeFragment, MutableMapping[
                FragmentView, FragmentReferenceFrame]]] = WeakKeyDictionary()

    # Instance variable containing a reference to the views ensemble a view belongs to
    __views_catalogue__: MutableMapping[FragmentView, FragmentReferenceFrame]

    def __init__(self, src: CodeFragment, begin: int = 0, end: int = 0, offset: int = 0) -> None:
        """
        Generates a new code fragment-view backed by another code fragment.

        :param src: the assembly code fragment of which the new fragment will constitute a view
        :param begin: line number of the first line contained in the new fragment
        :param end: line number of the first line following the last contained in the new fragment
        :param offset: offset of the view inside the origin fragment
        :raises ValueError: when the fragment size would not fit inside the origin fragment
        """

        # Delegate consistency checks
        super().__init__(src, begin, end, offset)
        self.__origin__ = src

        if src not in FragmentView.__sources_catalogue__:
            # If this source fragment has never been seen before, add it to the shared catalogue and allocate the views
            # catalogue
            self.__views_catalogue__ = WeakKeyDictionary()
            FragmentView.__sources_catalogue__[src] = self.__views_catalogue__
        else:
            # Otherwise, set the local reference to the views catalogue associated with the provided source
            self.__views_catalogue__ = FragmentView.__sources_catalogue__[src]

        # Add the new view's metadata to the catalogue
        self.__views_catalogue__[self] = FragmentView.FragmentReferenceFrame(begin, end, offset)

    # Utility method used for updating all the views' metadata after a structural change
    def __grow__(self, growth_point: int, size: int) -> None:
        # Iterate over all the registered views for the current origin
        for view, frame in self.__views_catalogue__.items():
            mutated: bool = False
            begin, end, offset = frame

            # Check if begin/offset have to be shifted
            if begin >= growth_point and view != self:
                begin += size
                offset += size
                mutated = True

            # Check if end has to be shifted
            if end >= growth_point:
                end += size
                mutated = True

            # If any metadata changes were needed, update the catalogue
            if mutated:
                self.__views_catalogue__[view] = FragmentView.FragmentReferenceFrame(begin, end, offset)

    # Utility method for calculating a line's position inside the origin list, given its line number
    def __line_to_index__(self, line_number: int) -> int:
        frame = self.__views_catalogue__[self]

        # Verify that the calculated index falls within this fragment's range
        if not frame.begin <= line_number < frame.end:
            raise IndexError("Index out of range")

        return line_number - self.get_begin() + self.get_offset()

    def get_begin(self) -> int:
        return self.__views_catalogue__[self].begin

    def get_end(self) -> int:
        return self.__views_catalogue__[self].end

    def get_offset(self) -> int:
        return self.__views_catalogue__[self].offset

    def slice(self, start: int, end: int) -> FragmentView:
        """
        Creates a new subview by slicing this one.

        The returned subview shares the same properties of any other view and is not in any way dependent from the
        parent, being merely a view of a contiguous subset of the statements contained therein.

        :param start: the starting line of the new fragment
        :param end: the end line of the new fragment
        :return: a FragmentView representing a slice of the contained statements
        :raises ValueError: when the specified interval doesn't fit inside the existing fragment
        """
        super().slice(start, end)
        return FragmentView(self.__origin__, start, end, self.__line_to_index__(start))

    def append(self, statement: Statement) -> None:
        self.__origin__.insert(self.get_offset() + len(self), statement)
        # Growth point is at the end of the slice
        self.__grow__(self.get_end(), 1)

    def extend(self, statements: List[Statement]) -> None:
        insertion_point = self.get_offset() + len(self)
        for st in statements:
            self.__origin__.insert(insertion_point, st)
            insertion_point += 1

        # Growth point is at the end of the slice
        self.__grow__(self.get_end(), len(statements))

    def insert(self, line_number: int, statement: Statement) -> None:
        self.__origin__.insert(self.__line_to_index__(line_number), statement)
        self.__grow__(line_number, 1)

    def pop(self, line_number: int = -1) -> Statement:
        if line_number == -1:
            line_number = self.get_end() - 1

        popping_point = self.__line_to_index__(line_number)
        popped = self.__origin__.pop(popping_point)
        self.__grow__(line_number, -1)
        return popped

    def copy(self) -> FragmentView:
        return FragmentView(src=self.__origin__, begin=self.get_begin(), end=self.get_end(), offset=self.get_offset())

    def clear(self) -> None:
        offset = self.get_offset()
        length = len(self)
        del self.__origin__[offset:offset + length]
        # View size shrinks to zero, with growth point set to end as not to influence this view's begin
        self.__grow__(self.get_end(), -length)

    def __iter__(self) -> Iterator[Statement]:
        curr = self.get_offset()
        stop = curr + len(self)

        while curr < stop:
            yield self.__origin__[curr]
            curr += 1

    def __len__(self) -> int:
        return self.get_end() - self.get_begin()

    # TODO add support for slices
    def __getitem__(self, line_number: int) -> Statement:
        return self.__origin__[self.__line_to_index__(line_number)]

    # TODO add support for slices
    def __setitem__(self, line_number: int, new_statement: Statement) -> None:
        self.__origin__[self.__line_to_index__(line_number)] = new_statement

    # TODO add support for slices
    def __delitem__(self, line_number: int) -> None:
        deletion_point = self.__line_to_index__(line_number)
        del self.__origin__[deletion_point]
        self.__grow__(line_number, -1)

    def __hash__(self) -> int:
        # IDs are unique for the entire life of an object, so no collisions should take place inside the shared
        # catalogue with this
        return hash((id(self), id(self.__origin__)))


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
            del d["role"]
            statements.append(constructor(labels=labs, **d))
            labs = []

    return Source(statements)
