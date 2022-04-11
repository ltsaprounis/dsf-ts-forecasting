# dsf-ts-forecasting
Time Series Forecasting in Python - Data Science Festival - GSK.  
:tv: the workshop recording is available here -> https://online.datasciencefestival.com/talks/workshop/

## Contents
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

## Additional Resources
* **VIDEOS:** 
  * [Prof Rob Hyndman - Uncertain futures: what can we forecast and when should we give up?](https://www.youtube.com/watch?v=YOeDTt_JJx0&t=3s)
  * [Any video on the YouTube channel of the Centre for Marketing Analytics and Forecasting](https://www.youtube.com/c/CentreforMarketingAnalyticsandForecasting)
  * [Sktime on PyData](https://www.youtube.com/watch?v=Wf2naBHRo8Q)
* **BLOGS & WEBSITES:**
  * [Hyndsight](https://robjhyndman.com/hyndsight/)
  * [Kouretzes](https://kourentzes.com/forecasting/category/blog/)
  * [International Institute of Forecasters](https://forecasters.org/)
* **BOOKS:**
  * [Forecasting: Principles and Practice (3rd ed)](https://otexts.com/fpp3/)
  * [Forecasting with Exponential Smoothing: the State Space Approach](https://robjhyndman.com/expsmooth/)
  * [Intermittent Demand Forecasting: Context, Methods and Applications](https://www.wiley.com/en-us/Intermittent+Demand+Forecasting:+Context,+Methods+and+Applications-p-9781119976080)
  * [Time Series Analysis by State Space Methods](https://oxford.universitypressscholarship.com/view/10.1093/acprof:oso/9780199641178.001.0001/acprof-9780199641178)

## References
1. Hyndman, R.J., & Athanasopoulos, G. (2021) Forecasting: principles and practice, 3rd edition, OTexts: Melbourne, Australia. https://otexts.com/fpp3/
