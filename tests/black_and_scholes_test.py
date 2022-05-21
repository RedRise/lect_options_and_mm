import src.black_scholes as bs

sigma = 0.2
x = 100
t = 0.5
K = 100
r = 0.01

def test_call_delta_value():

    cd = bs.call_delta(0.2, 100, 1, 0, 100)
    val = 0.5398
    assert abs(cd-val) < 0.0001

def test_call_put_parity_delta():
    
    cd = bs.call_delta(1,1,1,1,1)
    pd = bs.put_delta(1,1,1,1,1)

    assert cd - pd == 1

def test_call_gamma_value():

    cg = bs.call_gamma(0.2, 100, 1, 0.01, 100)
    
    assert abs(cg - 0.01972397) < 0.0001
    

def test_call_put_parity_gamma():
    
    cg = bs.call_gamma(1,1,1,1,1)
    pg = bs.put_gamma(1,1,1,1,1)

    assert cg == pg