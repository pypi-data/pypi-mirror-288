# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tsunami_ip_utils', 'tsunami_ip_utils.viz']

package_data = \
{'': ['*'],
 'tsunami_ip_utils': ['input_files/*'],
 'tsunami_ip_utils.viz': ['css/*']}

install_requires = \
['IPython',
 'dash',
 'flask',
 'h5py',
 'kaleido',
 'matplotlib',
 'openpyxl',
 'pandas',
 'plotly>=5.22.0,<5.23.0',
 'pyprojroot',
 'pytest',
 'pytest-mpl',
 'pyyaml',
 'scipy',
 'selenium',
 'tqdm',
 'uncertainties',
 'webdriver-manager']

setup_kwargs = {
    'name': 'tsunami-ip-utils',
    'version': '0.1.0',
    'description': 'A tool for visualizing similarity data from the SCALE code: TSUNAMI-IP',
    'long_description': 'Nothing here yet',
    'author': 'Matthew Louis',
    'author_email': 'matthewlouis31@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
