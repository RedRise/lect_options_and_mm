import src.option_hedger as oh
import src.black_scholes as bs

SIGMA = 0.2
K = 100
R = 0.01
T = 1


def test_simple_time_left():

    hedger = oh.OptionHedger(
        bs.call_delta_wrapper(SIGMA, K, R),
        T,
        R,
        0.5,
        1/365
    )

    hedger.update(100, 1)
    assert abs(hedger.delta - 0.55961) < 0.00001
    assert hedger.time_left == 1

    hedger.update(100, 0.5)
    assert abs(hedger.delta - 0.54223) < 0.00001
    assert hedger.time_left == 0.5
