# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rozetka',
 'rozetka.entities',
 'rozetka.examples',
 'rozetka.runners',
 'rozetka.tools']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-retry>=2.8.3,<3.0.0',
 'curl-cffi>=0.7.1,<0.8.0',
 'global-logger>=0.4.2,<0.5.0',
 'influxdb-client[async]>=1.44.0,<2.0.0',
 'knockknock>=0.1.8.1,<0.2.0.0',
 'pendulum>=3.0.0,<4.0.0',
 'progress>=1.6,<2.0',
 'python-worker>=2.2.2,<3.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.32.3,<3.0.0']

setup_kwargs = {
    'name': 'rozetka-api',
    'version': '1.6.6',
    'description': 'Rozetka Python API',
    'long_description': '[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)\n[![Made in Ukraine](https://img.shields.io/badge/made_in-Ukraine-ffd700.svg?labelColor=0057b7)](https://stand-with-ukraine.pp.ua)\n[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)\n[![Russian Warship Go Fuck Yourself](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/RussianWarship.svg)](https://stand-with-ukraine.pp.ua)\n\nRozetka.ua Python API\n---------------------\n[![PyPi Package](https://github.com/ALERTua/rozetka_api/actions/workflows/pypi.yml/badge.svg)](https://github.com/ALERTua/rozetka_api/actions/workflows/pypi.yml)\n[![Docker Image Latest](https://github.com/ALERTua/rozetka_api/actions/workflows/docker-image.yml/badge.svg)](https://github.com/ALERTua/rozetka_api/actions/workflows/docker-image.yml)\n\nHey-hey, Rozetka employee, I mean no harm. I just wanna know whether your discounts are real. Luvz.\n\nDo not forget to run with `--init` for SIGTERM to correctly forward to child processes.\n\n### Github\nhttps://github.com/ALERTua/rozetka_api\n\n### PyPi\nhttps://pypi.org/project/rozetka-api\n\n### Examples\n\n[examples/example_item.py](rozetka/examples/example_item.py)\n\n[examples/example_category.py](rozetka/examples/example_category.py)\n\n[tests/test_suite.py](tests/test_suite.py)\n',
    'author': 'Alexey ALERT Rubasheff',
    'author_email': 'alexey.rubasheff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ALERTua/rozetka_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
