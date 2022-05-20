import src.payoffs as payoffs

def test_call_90_100_is_zero():
    assert payoffs.call(90, 100) == 0

def test_call_110_100_is_10():
    assert payoffs.call(110, 100) == 10

def test_put_90_100_is_10():
    assert payoffs.put(90, 100) == 10

def test_put_110_100_is_zero():
    assert payoffs.put(110, 100) == 0

def test_straddle_is_10():
    assert payoffs.straddle(110, 100) == 10
    assert payoffs.straddle(90, 100) == 10