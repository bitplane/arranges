from arranges import Ranges


def test_slice_infinite_range():
    """Test slicing an infinite range"""
    r = Ranges("1:")  # 1 to infinity
    assert r[:10] == Ranges("1:10")
    assert r[5:15] == Ranges("5:15")
    assert r[20:] == Ranges("20:")


def test_slice_finite_range():
    """Test slicing a finite range"""
    r = Ranges("0:100")
    assert r[:50] == Ranges("0:50")
    assert r[25:75] == Ranges("25:75")
    assert r[50:] == Ranges("50:100")
    assert r[150:200] == Ranges("")  # Outside range


def test_slice_multiple_segments():
    """Test slicing ranges with multiple segments"""
    r = Ranges("0:10,20:30,40:50")
    assert r[:25] == Ranges("0:10,20:25")
    assert r[5:45] == Ranges("5:10,20:30,40:45")
    assert r[25:] == Ranges("25:30,40:50")
