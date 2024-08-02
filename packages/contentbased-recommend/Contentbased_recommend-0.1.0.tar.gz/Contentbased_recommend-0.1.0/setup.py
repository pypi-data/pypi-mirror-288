# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['content_based']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=2.0.31,<3.0.0',
 'pyodbc>=5.1.0,<6.0.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'torch>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'contentbased-recommend',
    'version': '0.1.0',
    'description': '',
    'long_description': "# TCC DMS Recommender System\n\n## Introduction\nThe project is structured as a GitLab repository for the DMS Recommender service. We're providing all types of recommender including, collaborative filtering, content-based, market basket analysis. Developers can choose any type of the recommender based on the use cases and user onboarding time period. For example, new user can apply, such as, content-based and market basket analysis. In later phase, collaborative filtering can be used.\n\n## Installation\n```bash\npip install ...\n```\n\n## Example Usage\n\n### Content-based recommendation\nIt is recommended to use when new users are onboarding in the platform.\n```python\n# set up  the recommender (connect DB and choose tables)\n\n# see all available categories or sub-categories\n\n# prepare user preference for categories and sub-categories with top K (using category or sub-category IDs)\n# without K, default is ...\n\n# create top products list for this customers with relevant scores\n\n# Now, apply these list with your app\n```\n\n### Market Basket Analysis\nIt is recommended to use when new users are onboarding in the platform.\n```python\n# set up recommender (connect DB and choose tables)\n\n# run analysis\n\n# see analysis result\n\n# export analysis result as .csv\n\n# inference the recommendations\n```\n\n### Collaborative filtering\nRecommended to use when users have purchasing history more than ... months or ... transactions. Also, routine updating model is mandatory.\n```python\n# set up recommender (connect DB and choose tables)\n```\nEnsure your database contains the following tables with appropriate data:\n\n- SKUMASTER\n- ICCAT\n- ICDEPT\n- TRANSTKD\n- GOODSMASTER\n```\n\n# run model training\n\n# see evaluation result\n\n# save model to path\n\n# inference the recommendations\n```",
    'author': 'Crparichaya',
    'author_email': 'parichaya.yan@ku.th',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
