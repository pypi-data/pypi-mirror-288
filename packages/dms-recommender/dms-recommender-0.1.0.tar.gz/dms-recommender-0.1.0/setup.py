# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dms_recommender',
 'dms_recommender.model',
 'dms_recommender.recommender',
 'dms_recommender.recommender.basket_analysis',
 'dms_recommender.recommender.collaborative',
 'dms_recommender.recommender.content_based',
 'dms_recommender.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0',
 'pandas>=2.2.2,<3.0.0',
 'pydantic>=2.8.2,<3.0.0',
 'scikit-learn>=1.5.1,<2.0.0',
 'torch==2.3.1',
 'transformers>=4.42.4,<5.0.0']

setup_kwargs = {
    'name': 'dms-recommender',
    'version': '0.1.0',
    'description': 'A recommendation system',
    'long_description': "# TCC DMS Recommender System\n\n## Introduction\nThe project is structured as a GitLab repository for the DMS Recommender service. We're providing all types of recommender including, collaborative filtering, content-based, market basket analysis. Developers can choose any type of the recommender based on the use cases and user onboarding time period. For example, new user can apply, such as, content-based and market basket analysis. In later phase, collaborative filtering can be used.\n\n## Installation\n```bash\npip install ...\n```\n\n## Example Usage\n\n### Content-based recommendation\nIt is recommended to use when new users are onboarding in the platform.\n```python\n# set up  the recommender (connect DB and choose tables)\n\n# see all available categories or sub-categories\n\n# prepare user preference for categories and sub-categories with top K (using category or sub-category IDs)\n# without K, default is ...\n\n# create top products list for this customers with relevant scores\n\n# Now, apply these list with your app\n```\n\n### Market Basket Analysis\nIt is recommended to use when new users are onboarding in the platform.\n```python\n# set up recommender (connect DB and choose tables)\n\n# run analysis\n\n# see analysis result\n\n# export analysis result as .csv\n\n# inference the recommendations\n```\n\n### Collaborative filtering\nRecommended to use when users have purchasing history more than ... months or ... transactions. Also, routine updating model is mandatory.\n```python\n# set up recommender (connect DB and choose tables)\n```\nEnsure your database contains the following tables with appropriate data:\n\n- SKUMASTER\n- ICCAT\n- ICDEPT\n- TRANSTKD\n- GOODSMASTER\n```\n\n# run model training\n\n# see evaluation result\n\n# save model to path\n\n# inference the recommendations\n```",
    'author': 'Cream',
    'author_email': 'cream.p@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
