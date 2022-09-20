# Options and Market Making (Lecture)

---

## Try on hosted environments

[![Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/RedRise/lect_options_and_mm) 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/RedRise/lect_options_and_mm/HEAD)

## Local Use

1. Install [Graphviz](https://www.graphviz.org/download).
2. Run ```. ./install/install.sh```.

## Local Run

- ```poetry run jupyter notebook```

---

## Content Description

Options Pricing and Market Making presentation material.

Sections are covered by jupyter notebooks.

### Intuition of pricing

- Averaging, expectation, pricing and replication
- Basic example of binomial 1-step model pricing
- ```01_intuition_of_pricing.ipynb```

### No Model Pricing

- Abscence of Arbitrage implication in pricing
- No model dependent
- Insight to pricing/probability duality
- ```02_no_model_pricing.ipynb```

### Binomial Model

- More detailed coverage of binomial model, 1-step and multistep
- ```03_binomial_model.ipynb```

### Continuous Model

- Introduction to continuous model
- Definition of stochastic integration
- Itô Lemma
- Basic exemples of option pricing using FTAP
- ```04_continuous_model.ipynb```

### Option hedging and Market Making

- Concrete overview of Call option pricing and greeks
- Replication portfolio example, and link to pricing
- Real life (not simulated) call replication
- Explanation of tracking error
- Link to market making
- ```05_call_option_mm.ipynb```

## About Diaporama notebook

1. Go to raw edition mode for notebook
2. Go to the ```metadata``` attribute (at the bottom)
3. It should contains :
   1. >"celltoolbar": "Diaporama"
   2. >"hide_input": false
