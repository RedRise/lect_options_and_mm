import numpy as np
from scipy.stats import norm


def d1(sigma, k, t, r, x):
    return (np.log(x/k) + (r+sigma**2/2)*t)/(sigma*np.sqrt(t))


def d2(sigma, k, t, r, x):
    return d1(sigma, k, t, r, x) - sigma*np.sqrt(t)


# Call option

def call_price(sigma, k, t, r, x):
    d1 = d1(sigma, k, t, r, x)
    d2 = d2(sigma, k, t, r, x)
    return norm.cdf(d1)*x-norm.cdf(d2)*k*np.exp(-r*t)


def call_delta(sigma, k, t, r, x):
    return norm.cdf(d1(sigma, k, t, r, x))


def call_gamma():
    return 0
    
# Put option

def put_price(sigma, k, t, r, x):
    return 0


def put_delta(sigma, k, t, r, x):
    return call_delta(sigma, k, t, r, x) - 1