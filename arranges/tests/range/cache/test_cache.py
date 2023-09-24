from arranges import Ranges


def test_cache_int_vs_list(test_id):
    from_zero = Ranges(test_id)
    list_value = Ranges([test_id])

    assert test_id in list_value

    assert from_zero == range(test_id)
    assert list_value == [test_id]
