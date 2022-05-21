from math import sqrt
import numpy as np
from numpy.random import default_rng

def geom_brownian_path(
    initPrice, 
    yearlyDrift, 
    yearlyVolat, 
    numDaysToSimul, 
    numStepPerDay: int = 1,
    seed = None):

    if initPrice < 0:
        raise ValueError("initPrice should be positive.")
        
    # initPrice = 100
    # yearlyDrift=0.1
    # yearlyVolat = 0.4
    # numDaysToSimul = 2000
    # numStepPerDay = 1
    numDaysPerYearConvention = 365
    
    dt = 1 / float(numDaysPerYearConvention * numStepPerDay)
    numSimul = numDaysToSimul * numStepPerDay

    rng = default_rng(seed)

    e = rng.normal(0, 1, numSimul-1)
    
    exponent = (yearlyDrift - 0.5 * yearlyVolat**2 )* dt + yearlyVolat * sqrt(dt) * e
    exponent = np.insert(exponent, 0, 0, axis=0)
    
    return (initPrice * np.exp(np.cumsum(exponent)), dt)