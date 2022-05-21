import numpy as np
from scipy.stats import norm


def d1(sigma, k, t, r, x):
    return (np.log(x/k) + (r+sigma**2/2)*t)/(sigma*np.sqrt(t))


def d2(sigma, k, t, r, x):
    return d1(sigma, k, t, r, x) - sigma*np.sqrt(t)


# Call option

def call_price(sigma, k, t, r, x):
    d1_val = d1(sigma, k, t, r, x)
    d2_val = d2(sigma, k, t, r, x)
    return norm.cdf(d1_val)*x-norm.cdf(d2_val)*k*np.exp(-r*t)


def call_delta(sigma, k, t, r, x):
    return norm.cdf(d1(sigma, k, t, r, x))


def call_gamma(sigma, k, t, r, x):
    numer = x * sigma * np.sqrt(t * 2 * np.pi)
    d1_val = d1(sigma, k, t, r, x)
    return np.exp(-d1_val**2/2) / numer


def call_vega(sigma, k, t, r, x):
    d1_val = d1(sigma, k, t, r, x)
    return x * np.sqrt(t / (2 * np.pi)) * np.exp(-d1_val**2/2)


# Put option


def put_price(sigma, k, t, r, x):
    d1_val = d1(sigma, k, t, r, x)
    d2_val = d2(sigma, k, t, r, x)
    return k*np.exp(-r*t)*norm.cdf(-d2_val) - norm.cdf(-d1_val)*x


def put_delta(sigma, k, t, r, x):
    return call_delta(sigma, k, t, r, x) - 1


put_gamma = call_gamma