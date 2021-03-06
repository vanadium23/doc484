"""
Module-level docs
"""

from __future__ import absolute_import, print_function


def basic(one, two, three, four, _five, six_):
    # type: (Union[str, int], str, Any, Any, bool, int) -> bool
    """
    Note that we escape before \six_ because underscore is a markdown
    character.  This is strictly to avoid warnings: the generated type comment
    will be correct with or without escaping.

    :param one: description of one
    :type one: Union[str, int]
    :param two: description of two
        that spans multiple lines
    :type two: str
    :param four:
    :param _five: description
        with

        a line break
    :type _five: bool
    :type \six_: int

    :rtype: bool
    :return: True if successful, False otherwise
    """


def star_args(one, *two, **three):
    # type: (Union[str, int], *str, **Any) -> bool
    """
    :type one: Union[str, int]
    :type two: str

    :rtype: bool
    """


def star_args2(one, *two, **three):
    # type: (Union[str, int], *str, **Any) -> bool
    """
    Note that we escape before \* because it is a markdown character.  This is
    strictly to avoid warnings: the generated type comment will be correct
    with or without escaping.

    :type one: Union[str, int]
    :type two: \*str

    :rtype: bool
    """


def skiptype(one, two, three):
    # notype
    """
    Use # notype comment to skip type comment generation

    :type one: Union[str, int]
    :type two: str

    :rtype: bool
    """


def no_doc_types(one, *two, **three):
    """
    Docstring with no types
    """


def no_docs(one, *two, **three):
    pass


def existing_type_comment(one, two, three):
    # type: (Union[str, int], str, Any) -> bool
    """
    Existing type comments should be overwritten

    :type one: Union[str, int]
    :type two: str

    :rtype: bool
    """


def existing_comment(one, two, three):
    # type: (Union[str, int], str, Any) -> bool
    # this comment should be preserved
    """
    :type one: Union[str, int]
    :type two: str

    :rtype: bool
    """


def default_return_type(one):
    # type: (str) -> Any
    """
    When no return type is specified, the default type can be globally
    configured.

    :type one: str
    """


def yields():
    """
    :yields: str
    """


class BasicClass:
    def foo(self, one, two, three):
        # type: (Union[str, int], str, Any) -> bool
        """
        :type one: Union[str, int]
        :type two: str

        :rtype: bool
        """


def function_self(self, one, two, three):
    # type: (Any, Union[str, int], str, Any) -> bool
    """
    A function with a first argument named self should document self

    :type one: Union[str, int]
    :type two: str

    :rtype: bool
    """


class InitDocsAtClassLevel:
    """
    Argument documentation at the class-level should be applied to __init__

    :type one: Union[str, int]
    :type two: str

    :rtype: bool
    """
    def __init__(self, one, two, three):
        # type: (Union[str, int], str, Any) -> bool
        pass
