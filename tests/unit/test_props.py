import pytest
import pleasehold


def test_begin_msg():
    with pleasehold.hold() as holding:
        assert holding.begin_msg == 'begin'
        holding.begin_msg = 'new'
        assert holding.begin_msg == 'new'

    with pleasehold.hold(begin_msg='ctor') as holding:
        assert holding.begin_msg == 'ctor'
        holding.begin_msg = 'new'
        assert holding.begin_msg == 'new'

    p1 = pleasehold.hold()
    assert p1.begin_msg == 'begin'
    p1.begin_msg = 'new'
    assert p1.begin_msg == 'new'

    p2 = pleasehold.hold(begin_msg='ctor_manual')
    assert p2.begin_msg == 'ctor_manual'
    p2.begin_msg = 'new'
    assert p2.begin_msg == 'new'


def test_end_msg():
    with pleasehold.hold() as holding:
        assert holding.end_msg == 'end'
        holding.end_msg = 'new'
        assert holding.end_msg == 'new'

    with pleasehold.hold(end_msg='ctor') as holding:
        assert holding.end_msg == 'ctor'
        holding.end_msg = 'new'
        assert holding.end_msg == 'new'

    p1 = pleasehold.hold()
    assert p1.end_msg == 'end'
    p1.end_msg = 'new'
    assert p1.end_msg == 'new'

    p2 = pleasehold.hold(end_msg='ctor_manual')
    assert p2.end_msg == 'ctor_manual'
    p2.end_msg = 'new'
    assert p2.end_msg == 'new'


def test_delay():
    with pleasehold.hold() as holding:
        assert holding.delay == 1.0
        holding.delay = 0.2
        assert holding.delay == 0.2

    with pleasehold.hold(delay=2) as holding:
        assert holding.delay == 2
        holding.delay = 2.1
        assert holding.delay == 2.1

    p1 = pleasehold.hold()
    assert p1.delay == 1.0
    p1.delay = 1.1
    assert p1.delay == 1.1

    p2 = pleasehold.hold(delay=3)
    assert p2.delay == 3
    p2.delay = 3.1
    assert p2.delay == 3.1


def test_symbol():
    with pleasehold.hold() as holding:
        assert holding.symbol == '.'
        holding.symbol = '#'
        assert holding.symbol == '#'

    with pleasehold.hold(symbol='$') as holding:
        assert holding.symbol == '$'
        holding.symbol = '%'
        assert holding.symbol == '%'

    p1 = pleasehold.hold()
    assert p1.symbol == '.'
    p1.symbol = 'apples'
    assert p1.symbol == 'apples'

    p2 = pleasehold.hold(symbol='!@#$')
    assert p2.symbol == '!@#$'
    p2.symbol = '\''
    assert p2.symbol == '\''
