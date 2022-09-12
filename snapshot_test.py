from snapshot import calculate_time, compare_list

def test_calculate_time():
    a = calculate_time("24h")
    b = calculate_time("12h")
    c = calculate_time("6h")
    d = calculate_time("4h")
    e = calculate_time("2h")

    assert a == 86400 and b == 43200 and c == 21600 and d == 14400 and e == 3600

def test_compare_list_equal():

    a = ["a", "b", "c", "d"]
    b = ["a", "b", "d", "c"]

    e = compare_list(a, b)
    assert len(e) == 0

def test_compare_list_smaller():
    a = ["a", "b", "c", "d"]
    b = ["a", "b", "d"]

    excluded = compare_list(a, b)
    assert "c" in excluded
