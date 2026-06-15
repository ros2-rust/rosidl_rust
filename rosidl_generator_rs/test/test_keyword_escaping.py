from rosidl_generator_rs import get_rs_name


def test_rust_keywords_are_escaped():
    for keyword in ("try", "type", "const", "async", "match"):
        assert get_rs_name(keyword) == f"{keyword}_"


def test_non_keyword_names_are_unchanged():
    assert get_rs_name("plain_field") == "plain_field"
