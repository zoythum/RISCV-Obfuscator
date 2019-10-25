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

    # Reference frame of the fragment
    begin: int
    end: int
    offset: int

    # Instance variable containing the list containing a certain code fragment
    _lines: List[Statement]

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

        self.begin = begin
        self.end = end
        self.offset = offset
        self._lines = list(src[offset:offset + end - begin])

    # Utility method for calculating a line's position inside the origin list, given its line number
    def _line_to_index(self, line_number: int) -> int:
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
        return FragmentCopy(self._lines, start, end, start - self.begin)

    def append(self, statement: Statement) -> None:
        self._lines.append(statement)
        self.end += 1

    def extend(self, statements: List[Statement]) -> None:
        self._lines.extend(statements)
        self.end += len(statements)

    def insert(self, line_number: int, statement: Statement) -> None:
        self._lines.insert(self._line_to_index(line_number), statement)
        self.end += 1

    def pop(self, line_number: int = -1) -> Statement:
        popped = self._lines.pop(self._line_to_index(line_number))
        self.end -= 1
        return popped

    def copy(self) -> FragmentCopy:
        """
        Makes a shallow copy of this fragment.

        :return: a shallow copy of this fragment
        """

        return FragmentCopy(self._lines, self.begin, self.end, self.offset)

    def clear(self) -> None:
        self._lines.clear()
        self.end = self.begin

    def __iter__(self) -> Iterator[Statement]:
        return self._lines.__iter__()

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, line_number: Union[int, slice]) -> Union[Statement, FragmentCopy]:
        """
        Access the contained statements through the Sequence interface.

        Due to the underlying implementation, access by slices only works if the extremes are included between the start
        and the end of this fragment.

        :param line_number: line number(s) to be targeted
        :return: the selected statement(s), encapsulated in a FragmentCopy in case of access by slices
        """
        if type(line_number) is int:
            return self._lines[self._line_to_index(line_number)]
        elif type(line_number) is slice:
            # We return a FragmentCopy representing the slice, but notice how the offset info gets lost
            return FragmentCopy(self._lines[self._line_to_index(line_number.start):
                                            self._line_to_index(line_number.stop):
                                            line_number.step],
                                line_number.start,
                                line_number.stop,
                                0)
        else:
            raise TypeError("Integer index or slice expected")

    def __setitem__(self, line_number: Union[int, slice], statement: Union[Statement, Sequence[Statement]]) -> None:
        """
        Modify the contained statements through the Sequence interface.

        Due to the underlying implementation, access by slices only works if the extremes are included between the start
        and the end of this fragment.

        :param line_number: line number(s) to be targeted
        :param statement: statement(s) to be set
        """
        if type(line_number) is int:
            self._lines[self._line_to_index(line_number)] = statement
        elif type(line_number) is slice:
            self._lines[self._line_to_index(line_number.start):
                        self._line_to_index(line_number.stop):
                        line_number.step] = statement

            if len(statement) == 0:
                # A funky deletion just took place, so we must treat it accordingly
                self.end -= line_number.stop - line_number.start
        else:
            raise TypeError("Integer index/statement or slice/list expected")

    def __delitem__(self, line_number: Union[int, slice]) -> None:
        """
        Delete the contained statements through the Sequence interface.

        Due to the underlying implementation, access by slices only works if the extremes are included between the start
        and the end of this fragment.

        :param line_number: line number(s) to be targeted
        """
        if type(line_number) is int:
            del self._lines[self._line_to_index(line_number)]
            self.end -= 1
        elif type(line_number) is slice:
            del self._lines[self._line_to_index(line_number.start):
                            self._line_to_index(line_number.stop):
                            line_number.step]

            # Decrease the list's size according to the number of elements that got deleted
            self.end -= len(range(line_number.start,
                                  line_number.stop,
                                  1 if line_number.step is None else line_number.step))
        else:
            raise TypeError("Integer index/statement or slice/list expected")

    def __hash__(self) -> int:
        # The embedded list's lifecycle is tightly coupled with the fragment's one, so this should suffice
        return hash((id(self), id(self._lines)))


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

    # Named tuple used for containing views' metadata (aka its reference frame)
    class FragmentReferenceFrame(NamedTuple):
        begin: int
        end: int
        offset: int

    # Declare and allocate the shared catalogue of source fragments
    _sources_catalogue: ClassVar[
        MutableMapping[
            CodeFragment, MutableMapping[
                FragmentView, FragmentReferenceFrame]]] = WeakKeyDictionary()

    # Instance variable containing a reference to the views ensemble a view belongs to
    _views_catalogue: MutableMapping[FragmentView, FragmentReferenceFrame]

    # Instance variable containing a reference to the backing fragment
    _origin: CodeFragment

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
        self._origin = src

        if src not in FragmentView._sources_catalogue:
            # If this source fragment has never been seen before, add it to the shared catalogue and allocate the views
            # catalogue
            self._views_catalogue = WeakKeyDictionary()
            FragmentView._sources_catalogue[src] = self._views_catalogue
        else:
            # Otherwise, set the local reference to the views catalogue associated with the provided source
            self._views_catalogue = FragmentView._sources_catalogue[src]

        # Add the new view's metadata to the catalogue
        self._views_catalogue[self] = FragmentView.FragmentReferenceFrame(begin, end, offset)

    # Utility method used for updating all the views' metadata after a structural change
    def _grow(self, growth_point: int, size: int) -> None:
        # Iterate over all the registered views for the current origin
        for view, frame in self._views_catalogue.items():
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
                self._views_catalogue[view] = FragmentView.FragmentReferenceFrame(begin, end, offset)

    # Utility method for calculating a line's position inside the origin list, given its line number
    def _line_to_index(self, line_number: int) -> int:
        frame = self._views_catalogue[self]

        # Verify that the calculated index falls within this fragment's range
        if not frame.begin <= line_number < frame.end:
            raise IndexError("Index out of range")

        return line_number - self.get_begin() + self.get_offset()

    def get_begin(self) -> int:
        return self._views_catalogue[self].begin

    def get_end(self) -> int:
        return self._views_catalogue[self].end

    def get_offset(self) -> int:
        return self._views_catalogue[self].offset

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
        return FragmentView(self._origin, start, end, self._line_to_index(start))

    def append(self, statement: Statement) -> None:
        self._origin.insert(self.get_offset() + len(self), statement)
        # Growth point is at the end of the slice
        self._grow(self.get_end(), 1)

    def extend(self, statements: List[Statement]) -> None:
        insertion_point = self.get_offset() + len(self)
        for st in statements:
            self._origin.insert(insertion_point, st)
            insertion_point += 1

        # Growth point is at the end of the slice
        self._grow(self.get_end(), len(statements))

    def insert(self, line_number: int, statement: Statement) -> None:
        self._origin.insert(self._line_to_index(line_number), statement)
        self._grow(line_number, 1)

    def pop(self, line_number: int = -1) -> Statement:
        if line_number == -1:
            line_number = self.get_end() - 1

        popping_point = self._line_to_index(line_number)
        popped = self._origin.pop(popping_point)
        self._grow(line_number, -1)
        return popped

    def copy(self) -> FragmentView:
        return FragmentView(src=self._origin, begin=self.get_begin(), end=self.get_end(), offset=self.get_offset())

    def clear(self) -> None:
        offset = self.get_offset()
        length = len(self)
        del self._origin[offset:offset + length]
        # View size shrinks to zero, with growth point set to end as not to influence this view's begin
        self._grow(self.get_end(), -length)

    def __iter__(self) -> Iterator[Statement]:
        curr = self.get_offset()
        stop = curr + len(self)

        while curr < stop:
            yield self._origin[curr]
            curr += 1

    def __len__(self) -> int:
        return self.get_end() - self.get_begin()

    def __getitem__(self, line_number: Union[int, slice]) -> Union[Statement, FragmentView]:
        """
        Access the contained statements through the Sequence interface.

        Due to the underlying implementation, access by slices only works if the extremes are included between the start
        and the end of this fragment.

        :param line_number: line number(s) to be targeted
        :return: the selected statement(s), encapsulated in a FragmentView in case of access by slices
        """
        if type(line_number) is int:
            return self._origin[self._line_to_index(line_number)]
        elif type(line_number) is slice:

            if line_number.step is not None:
                # Nothing like sparse views exist, so reject extended slices
                raise ValueError("'step' not supported by views")
            elif line_number.start < self.get_begin() or line_number.stop > self.get_end():
                # We don't support slice truncation, so we reject slices not fitting inside the fragment
                raise ValueError("Slice exceeds fragment size")

            return FragmentView(self._origin,
                                line_number.start,
                                line_number.stop,
                                self.get_offset() + line_number.start - self.get_begin())
        else:
            raise TypeError("Integer index or slice expected")

    def __setitem__(self, line_number: Union[int, slice], statement: Union[Statement, Sequence[Statement]]) -> None:
        """
        Modify the contained statements through the Sequence interface.

        Due to the underlying implementation, access by slices only works if the extremes are included between the start
        and the end of this fragment.

        :param line_number: line number(s) to be targeted
        :param statement: statement(s) to be set
        """
        if type(line_number) is int:
            self._origin[self._line_to_index(line_number)] = statement
        elif type(line_number) is slice:
            # Be aware of the ugly workaround used to let _line_to_index() process a slice reaching the end of the
            # fragment. Without the decrement-call-increment, it would report an IndexError
            start = self._line_to_index(line_number.start)
            stop = self._line_to_index(line_number.stop - 1) + 1 if line_number.stop == self.get_end() \
                else self._line_to_index(line_number)
            self._origin[start:stop:line_number.step] = statement

            if len(statement) == 0:
                # A funky deletion just took place, so we must treat it appropriately
                self._grow(self._line_to_index(line_number.start), -(line_number.stop - line_number.start))
        else:
            raise TypeError("Integer index or slice expected")

    def __delitem__(self, line_number: Union[int, slice]) -> None:
        """
        Delete the contained statements through the Sequence interface.

        Due to the underlying implementation, access by slices only works if the extremes are included between the start
        and the end of this fragment.

        :param line_number: line number(s) to be targeted
        """
        if type(line_number) is int:
            deletion_point = self._line_to_index(line_number)
            del self._origin[deletion_point]
            self._grow(line_number, -1)
        elif type(line_number) is slice:
            # Be aware of the ugly workaround used to let _line_to_index() process a slice reaching the end of the
            # fragment. Without the decrement-call-increment, it would report an IndexError
            start = self._line_to_index(line_number.start)
            stop = self._line_to_index(line_number.stop - 1) + 1 if line_number.stop == self.get_end() \
                else self._line_to_index(line_number)
            del self._origin[start:stop:line_number.step]

            # Decrease the list's size according to the number of elements that got deleted
            self._grow(line_number.start, -len(range(line_number.start, line_number.stop, line_number.step)))
        else:
            raise TypeError("Integer index/statement or slice/list expected")

    def __hash__(self) -> int:
        # IDs are unique for the entire life of an object, so no collisions should take place inside the shared
        # catalogue with this
        return hash((id(self), id(self._origin)))


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
