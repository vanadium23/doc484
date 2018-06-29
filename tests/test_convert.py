from __future__ import absolute_import, print_function

import pytest
from lib2to3.refactor import RefactoringTool, get_fixers_from_package
from doc484.__main__ import main


def convert_string(input):
    tool = RefactoringTool(get_fixers_from_package("doc484.fixes"))
    tree = tool.refactor_string(input, '<test.py>')
    return str(tree)


@pytest.mark.parametrize("config", ['test1', 'test2'])
@pytest.mark.parametrize("format", ['numpydoc'])
def test_cli(format, config, pytestconfig, tmpdir):
    print(format, config)
    fixturedir = pytestconfig.rootdir.join('tests', 'fixtures')

    configdir = fixturedir.join('configs', config)
    results = fixturedir.join('results', '%s.%s.py' % (format, config))
    source = fixturedir.join('formats', (format + '.py'))
    # change directory so we can control discovery of setup.cfg
    configdir.chdir()
    dest = tmpdir.join((format + '.py'))

    main(["--write", "--nobackups", "--no-diffs", "--output-dir",
          str(tmpdir), str(source)])

    with dest.open() as f:
        destlines = f.read()

    if results.exists():
        with results.open() as f:
            expectedlines = f.read()
    else:
        print(destlines)
        expectedlines = ''

    assert expectedlines == destlines


def test_basic():
    input = '''\
def basic(one, two, three, four, five, six):
    """
    Parameters
    ----------
    one : Union[str, int]
        description of one
    two : str
        description of two
        that spans multiple lines

    four
        omitted type
    five : bool
        description
        with

        a line break
    six : int

    Return
    ------
    bool
    """
'''
    output = convert_string(input)

    expected = '''\
def basic(one, two, three, four, five, six):
    # type: (Union[str, int], str, Any, Any, bool, int) -> bool
    """
    Parameters
    ----------
    one : Union[str, int]
        description of one
    two : str
        description of two
        that spans multiple lines

    four
        omitted type
    five : bool
        description
        with

        a line break
    six : int

    Return
    ------
    bool
    """
'''
    assert output == expected


def test_omit_type():
    input = '''\
"""
Module-level docs
"""

def foo(one, two, three):
    """
    Parameters
    ----------
    one
    two : str

    Return
    ------
    bool
    """
    pass
'''
    output = convert_string(input)

    expected = '''\
"""
Module-level docs
"""

def foo(one, two, three):
    # type: (Any, str, Any) -> bool
    """
    Parameters
    ----------
    one
    two : str

    Return
    ------
    bool
    """
    pass
'''
    assert output == expected


def test_star_args():
    # Not necessary for mypy but useful for PyCharm

    input = '''\
def foo(one, *two, **three):
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str

    Return
    ------
    bool
    """
    pass
'''
    output = convert_string(input)

    expected = '''\
def foo(one, *two, **three):
    # type: (Union[str, int], *str, **Any) -> bool
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str

    Return
    ------
    bool
    """
    pass
'''
    assert output == expected


def test_star_args2():
    # Not necessary for mypy but useful for PyCharm

    input = '''\
def foo(one, *two, **three):
    """
    Parameters
    ----------
    one : Union[str, int]
    two : *str

    Return
    ------
    bool
    """
    pass
'''
    output = convert_string(input)

    expected = '''\
def foo(one, *two, **three):
    # type: (Union[str, int], *str, **Any) -> bool
    """
    Parameters
    ----------
    one : Union[str, int]
    two : *str

    Return
    ------
    bool
    """
    pass
'''
    assert output == expected


def test_notype():
    input = '''\
def foo(one, two, three):
    # notype
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str

    Return
    ------
    bool
    """
    pass
'''
    output = convert_string(input)

    assert output == input


def test_no_doc_types():
    input = '''\
def foo(one, *two, **three):
    """
    Description of foo
    """
    pass
'''
    output = convert_string(input)

    assert output == input


def test_default_return_type():
    input = '''\
def foo(one):
    """
    Description of foo
    
    Parameters
    ----------
    one : str
    """
    pass
'''
    output = convert_string(input)

    assert output == '''\
def foo(one):
    # type: (str) -> Any
    """
    Description of foo
    
    Parameters
    ----------
    one : str
    """
    pass
'''


def test_class():
    input = '''\
class Bar:
    def foo(self, one, two, three):
        """
        Parameters
        ----------
        one : Union[str, int]
        two : str
    
        Return
        ------
        bool
        """
        pass
'''
    output = convert_string(input)

    expected = '''\
class Bar:
    def foo(self, one, two, three):
        # type: (Union[str, int], str, Any) -> bool
        """
        Parameters
        ----------
        one : Union[str, int]
        two : str
    
        Return
        ------
        bool
        """
        pass
'''
    assert output == expected


def test_function_self():
    input = '''\
def foo(self, one, two, three):
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str

    Return
    ------
    bool
    """
    pass
'''
    output = convert_string(input)

    expected = '''\
def foo(self, one, two, three):
    # type: (Any, Union[str, int], str, Any) -> bool
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str

    Return
    ------
    bool
    """
    pass
'''
    assert output == expected


def test_class_init_docs():
    input = '''\
class Foo:
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str
    """
    def __init__(self, one, two, three):
        pass
'''
    output = convert_string(input)

    expected = '''\
class Foo:
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str
    """
    def __init__(self, one, two, three):
        # type: (Union[str, int], str, Any) -> None
        pass
'''
    assert output == expected


def test_class_init_no_change():
    input = '''\
class Foo:
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str
    """
    def __init__(self, one, two, three):
        pass
'''
    output = convert_string(input)

    expected = '''\
class Foo:
    """
    Parameters
    ----------
    one : Union[str, int]
    two : str
    """
    def __init__(self, one, two, three):
        # type: (Union[str, int], str, Any) -> None
        pass
'''
    assert output == expected


