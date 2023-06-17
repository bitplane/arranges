from arranges import Range


def test_repr_empty():
    assert repr(Range("")) == "Range(0, 0)"


def test_repr_full():
    assert repr(Range(":")) == "Range(0, inf)"


def test_repr_stop_only():
    assert repr(Range("  102")) == "Range(102, 103)"
    assert repr(Range(":123")) == "Range(123)"


def test_repr_start_only():
    assert repr(Range("  102:")) == "Range(102, inf)"


def test_repr_start_and_stop():
    assert repr(Range("  102 : 123  ")) == "Range(102, 123)"


def test_str_empty():
    assert str(Range("")) == ""


def test_str_full():
    assert str(Range(":")) == ":"


def test_str_stop_only():
    assert str(Range(":123")) == ":123"


def test_str_start_only():
    assert str(Range("  102:")) == "102:"


def test_str_single_number():
    assert str(Range("  102")) == "102"


def test_str_start_and_stop():
    assert str(Range("  102 : 123  ")) == "102:123"
