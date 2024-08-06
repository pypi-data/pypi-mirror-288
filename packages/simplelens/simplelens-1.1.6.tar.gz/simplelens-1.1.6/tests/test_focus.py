from pytest import raises
import lens


def test_focus():
    collection = {'a': ['aye', 'ah'], 'b': ('be', 'bee'), 'c': {'words': ['sea', 'see']}}
    assert lens.focus(collection, ['a', 0]) == 'aye'
    assert lens.focus(collection, ['b', 1]) == 'bee'
    assert lens.focus(collection, ['c', 'words', 0]) == 'sea'


def test_focus_with_default():
    collection = {'a': ['aye', 'ah'], 'b': ('be', 'bee'), 'c': {'words': ['sea', 'see']}}
    default = 'yolo'
    assert lens.focus(collection, ['z'], default_result=default) == default


def test_focus_without_default():
    collection = {'a': ['aye', 'ah'], 'b': ('be', 'bee'), 'c': {'words': ['sea', 'see']}}
    with raises(lens.FocusingError):
        lens.focus(collection, ['z'])


def test_multi_focus():
    collection = {'a': ['aye', 'ah'], 'b': ('be', 'bee'), 'c': {'words': ['sea', 'see']}}
    expected_result = ('ah', 'bee', 'sea')
    observed_result = lens.multi_focus(collection=collection, keys=(['a', 1], ['b', 1], ['c', 'words', 0]))
    assert observed_result == expected_result
