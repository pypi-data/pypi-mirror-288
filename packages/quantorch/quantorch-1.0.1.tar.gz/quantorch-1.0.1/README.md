<div align=center>
<img src="assets/img/quantorch_logo.png" width="40%" loc>
</div>

<div align=center>
  
# QuanTorch : High-Performance Torch Library for Derivatives Pricing

[![Build Status](https://img.shields.io/github/actions/workflow/status/jialuechen/quantorch/python-package.yml)](https://github.com/jialuechen/quantorch/actions)
[![PyPI version](https://img.shields.io/pypi/v/quantorch)](https://pypi.org/project/quantorch/)
[![License](https://img.shields.io/github/license/jialuechen/quantorch)](https://github.com/jialuechen/quantorch/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/quantorch)](https://pypi.org/project/quantorch/)
[![Docs Status](https://readthedocs.org/projects/quantorch/badge/?version=latest)](https://quantorch.readthedocs.io/en/latest/)
![Python versions](https://img.shields.io/badge/python-3.6%2B-green)

</div>

QuanTorch is a comprehensive derivatives pricing library built on top of PyTorch. It provides a range of tools for asset pricing, risk management, and model calibration based on PyTorch's GPU accelerateion and automatic differentiation.

## Features

- **Asset Pricing**:
  - Option pricing models including Black-Scholes-Merton, binomial tree, and Monte Carlo simulations.
  - Bond pricing models including callable, putable, and convertible bonds.
  - Advanced options support including American, Bermudan, Asian, barrier and look-back options.
  - Implied volatility calculation using "Let's be rational" algorithm.
  - Futures and currency pricing.

- **Risk Management**:
  - Greeks calculation including Malliavin calculus.
  - Scenario analysis and stress testing.
  - Market risk measures such as VaR and Expected Shortfall.
  - Credit risk models including structural and reduced form models.
  - Valuation adjustments (CVA, DVA, MVA, FVA).

- **Model Calibration**:
  - Calibration for stochastic models like Heston, Vasicek, SABR, and more.
  - Local volatility models including Dupire.

- **Machine Learning and Reinforcement Learning**:
  - Regression and classification models using PyTorch.
  - Reinforcement learning examples.

## Installation

You can install QuanTorch via pip:

```bash
pip install quantorch
```

## Usage (check out the examples folder for more information)

### Exotic Options

#### American Option

```python
import torch
from quantorch.core.asset_pricing.option_pricing.american_option import american_option

spot = torch.tensor(100.0)
strike = torch.tensor(105.0)
expiry = torch.tensor(1.0)
volatility = torch.tensor(0.2)
rate = torch.tensor(0.05)
steps = 100

price = american_option('call', spot, strike, expiry, volatility, rate, steps)
print(f'American Option Price: {price.item()}')
```

#### Bermudan Option

```python
import torch
from quantorch.core.asset_pricing.option_pricing.bermudan_option import bermudan_option

spot = torch.tensor(100.0)
strike = torch.tensor(105.0)
expiry = torch.tensor(1.0)
volatility = torch.tensor(0.2)
rate = torch.tensor(0.05)
steps = 100
exercise_dates = torch.tensor([30, 60, 90])

price = bermudan_option('call', spot, strike, expiry, volatility, rate, steps, exercise_dates)
print(f'Bermudan Option Price: {price.item()}')
```

#### Asian Option

```python
import torch
from quantorch.core.asset_pricing.option_pricing.asian_option import asian_option

spot = torch.tensor(100.0)
strike = torch.tensor(105.0)
expiry = torch.tensor(1.0)
volatility = torch.tensor(0.2)
rate = torch.tensor(0.05)
steps = 100

price = asian_option('call', spot, strike, expiry, volatility, rate, steps)
print(f'Asian Option Price: {price.item()}')
```

### Greeks Calculation using Malliavin Calculus

```python
import torch
from quantorch.risk_management.greeks.malliavin import malliavin_greek

option_price = torch.tensor(10.0)
underlying_price = torch.tensor(100.0)
volatility = torch.tensor(0.2)
expiry = torch.tensor(1.0)

greek = malliavin_greek(option_price, underlying_price, volatility, expiry)
print(f'Malliavin Greek: {greek.item()}')
```

### Model Calibration

#### Heston Model Calibration

```python
import torch
from quantorch.calibration.heston_calibration import calibrate_heston

market_prices = torch.tensor([10.0, 12.0, 14.0, 16.0])
strikes = torch.tensor([100.0, 105.0, 110.0, 115.0])
expiries = torch.tensor([1.0, 1.0, 1.0, 1.0])
spot = torch.tensor(100.0)
rate = torch.tensor(0.05)

params = calibrate_heston(market_prices, strikes, expiries, spot, rate)
print(f'Calibrated Heston Parameters: {params}')
```

## Roadmap


### Q4 2024
- Develop an interactive dashboard for visualizing risk metrics and option pricing.

### Q3 2025
- Add support for more asset classes such as commodities and real estate.
- Enhance the calibration module to support a broader range of models and optimization techniques.

## Development

To contribute to QuanTorch, clone the repository and install the required dependencies:

```bash
git clone https://github.com/jialuechen/quantorch.git
cd quantorch
pip install -r requirements.txt
```

Run the tests to ensure everything is working:

```bash
pytest
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
