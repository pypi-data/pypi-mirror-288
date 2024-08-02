# TCC DMS Recommender System

## Introduction
The project is structured as a GitLab repository for the DMS Recommender service. We're providing all types of recommender including, collaborative filtering, content-based, market basket analysis. Developers can choose any type of the recommender based on the use cases and user onboarding time period. For example, new user can apply, such as, content-based and market basket analysis. In later phase, collaborative filtering can be used.

## Installation
```bash
pip install ...
```

## Example Usage

### Content-based recommendation
It is recommended to use when new users are onboarding in the platform.
```python
# set up  the recommender (connect DB and choose tables)

# see all available categories or sub-categories

# prepare user preference for categories and sub-categories with top K (using category or sub-category IDs)
# without K, default is ...

# create top products list for this customers with relevant scores

# Now, apply these list with your app
```

### Market Basket Analysis
It is recommended to use when new users are onboarding in the platform.
```python
# set up recommender (connect DB and choose tables)

# run analysis

# see analysis result

# export analysis result as .csv

# inference the recommendations
```

### Collaborative filtering
Recommended to use when users have purchasing history more than ... months or ... transactions. Also, routine updating model is mandatory.
```python
# set up recommender (connect DB and choose tables)
```
Ensure your database contains the following tables with appropriate data:

- SKUMASTER
- ICCAT
- ICDEPT
- TRANSTKD
- GOODSMASTER
```

# run model training

# see evaluation result

# save model to path

# inference the recommendations
```