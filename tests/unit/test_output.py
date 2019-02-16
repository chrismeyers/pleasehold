import time
from collections import Counter
import pytest
import pleasehold

def test_push(capsys):
    duration = 2
    push_msg = 'push'
    with pleasehold.hold() as holding:
        holding.push(push_msg)
        time.sleep(duration)
    captured = capsys.readouterr()

    # The first line of stdout contains the escape sequence that clears the line
    stdout = captured.out.split('\n')

    assert stdout[1] == push_msg


def test_symbols(capsys):
    duration = 2
    symbol = None
    delay = -1
    with pleasehold.hold() as holding:
        symbol = holding.symbol
        delay = holding.delay
        time.sleep(duration)
    captured = capsys.readouterr()
    c = Counter(captured.out)

    assert c[symbol] == duration * delay
