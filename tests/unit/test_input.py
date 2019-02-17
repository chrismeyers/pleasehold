import time
from collections import Counter
import pytest
import pleasehold


def test_push_from_input(capsys, monkeypatch):
    duration = 2
    input_msg = 'mock'

    monkeypatch.setattr('builtins.input', lambda x: input_msg)

    with pleasehold.hold() as holding:
        time.sleep(duration)
        with pleasehold.transfer(holding):
            stdin = input(input_msg)
        holding.push(stdin)
        time.sleep(duration)
    captured = capsys.readouterr()

    # The first line of stdout contains the begin msg and loading ticks
    # The second line of stdout contains the clear line escape sequence
    stdout = captured.out.split('\n')

    assert stdout[2] == input_msg


def test_symbols_after_input(capsys, monkeypatch):
    # The number of symbols generated is sometimes one greater than expected.
    # This is because the loading thread is sometimes in the middle of a tick
    # when input is requested.
    #
    # Increase the range to stress test this.
    for _ in range(100):
        _symbols_after_input(capsys, monkeypatch)


def _symbols_after_input(capsys, monkeypatch):
    duration = 2
    sleeps = 0
    input_msg = 'mock'
    symbol = None
    delay = -1

    monkeypatch.setattr('builtins.input', lambda x: input_msg)

    with pleasehold.hold() as holding:
        symbol = holding.symbol
        delay = holding.delay
        time.sleep(duration)
        sleeps += 1
        with pleasehold.transfer(holding):
            stdin = input(input_msg)
        holding.push(stdin)
        time.sleep(duration)
        sleeps += 1
    captured = capsys.readouterr()

    stdout = captured.out.strip().split('\n')
    c = Counter(stdout[-1])

    assert c[symbol] == int((delay * duration) * sleeps)
