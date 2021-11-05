# dsf-ts-forecasting
Time Series Forecasting in Python - Data Science Festival - GSK

**Contents:**
* Time Series EDA
* Naive Benchmarks
* Evaluation metrics
* Time Series Cross Validation 
* Statistical Methods - Exponential Smoothing, ARIMA, TBATS
* Machine Learning for time-series forecasting
  * direct approach
  * recursive features
  * global forecasting models 

## Quickstart
1. Create a python virtual environment:  
`python -m venv .venv`
2. Activate your environment:  
`source .venv/bin/activate`
3. If you want install the development requirements:  
`pip install -r requirements.dev.txt`
4. Install pre-commit to use pre-commit hooks:
`pre-commit install`
5. Install the package in development mode:  
`pip install -e .`

OR

1. `make environment`
2. `source .venv/bin/activate`

## Data
Data was downloaded from the [CDC - Flu portal dashboard](https://gis.cdc.gov/grasp/fluview/fluportaldashboard.html)

## References
1. Hyndman, R.J., & Athanasopoulos, G. (2021) Forecasting: principles and practice, 3rd edition, OTexts: Melbourne, Australia. https://otexts.com/fpp3/
