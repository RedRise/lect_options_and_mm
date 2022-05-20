import src.black_scholes as bs

sigma = 0.2
x = 100
t = 0.5
K = 100
r = 0.01

def test_call_put_parity_delta():
    
    cd = bs.call_delta(1,1,1,1,1)
    pd = bs.put_delta(1,1,1,1,1)

    assert cd - pd == 1