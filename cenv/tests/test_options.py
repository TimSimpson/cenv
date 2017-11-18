from cenv import options


def test_options():
    # type: () -> None
    op = options.Options()
    assert op is not None
