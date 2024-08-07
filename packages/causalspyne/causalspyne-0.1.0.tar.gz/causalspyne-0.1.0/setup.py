# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causalspyne']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.9.1,<4.0.0',
 'networkx>=3.2.1,<4.0.0',
 'numpy>=2.0.1,<3.0.0',
 'pandas>=2.2.2,<3.0.0',
 'pygraphviz>=1.11,<2.0',
 'scipy>=1.11.4,<2.0.0']

setup_kwargs = {
    'name': 'causalspyne',
    'version': '0.1.0',
    'description': 'hierarchical data generation for causal discovery and abstraction',
    'long_description': '# ProblemSetApproximateCausalDiscovery\n\n```\nfrom causalspyne import gen_partially_observed\n\n\ngen_partially_observed(size_micro_node_dag=4,     \n                       num_macro_nodes=4,\n                       degree=2,  # average vertex/node degree\n                       list_confounder2hide=[0.5, 0.9], # choie of confounder to hide: percentile or index of all toplogically sorted confounders \n                       num_sample=200)\n```\n',
    'author': 'Xudong Sun, Alex Markham',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
