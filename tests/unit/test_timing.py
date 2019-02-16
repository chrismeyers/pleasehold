import time
import math
import pytest
import pleasehold

def test_duration():
    duration = 5
    begin = time.time()
    with pleasehold.hold():
        time.sleep(duration)
    total = time.time() - begin

    assert math.isclose(total, duration, rel_tol=0.01)
