import src.paths as p
import numpy as np

def test_path_len():
    path, _ = p.geom_brownian_path(100, 0.1, 0.2, 100, 1)
    assert len(path) == 100

def test_path_init_price():
    path, _ = p.geom_brownian_path(100, 0.1, 0.2, 100, 1)
    assert path[0] == 100
    
def test_path_volatility():
    path, _ = p.geom_brownian_path(100, 0, 0.1, 365, 1, 201)
    vol = np.diff(np.log(path)).std()*np.sqrt(365)
    assert 0.09 < vol
    assert vol < 0.11