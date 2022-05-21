import src.paths as p


def test_path_len():
    path = p.geom_brownian_path(100, 0.1, 0.2, 100, 1)
    assert len(path) == 100

def test_path_init_price():
    path = p.geom_brownian_path(100, 0.1, 0.2, 100, 1)
    assert path[0] == 100
    