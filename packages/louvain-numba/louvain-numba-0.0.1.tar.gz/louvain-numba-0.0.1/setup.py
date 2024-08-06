# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['louvain_numba']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.1.0,<4.0.0',
 'numba>=0.58.1,<0.59.0',
 'numpy>=1.26.2,<2.0.0',
 'scipy>=1.11.2,<2.0.0']

setup_kwargs = {
    'name': 'louvain-numba',
    'version': '0.0.1',
    'description': 'A package for fast community detection in graphs using the Louvain method with Numba optimization.',
    'long_description': '# Louvain-Numba\n\nLouvain-Numba is a Python library for community detection in graphs using the Louvain method with Numba optimization. This library leverages Numba to accelerate the community detection process, making it suitable for large-scale graphs.\n\n## Features\n\n- Efficient community detection using the Louvain method\n- Optimized with Numba for high performance\n- Supports various graph input types (NetworkX, NumPy arrays, SciPy sparse matrices)\n- Generates hierarchical community structures\n\n## Installation\n\nYou can install Louvain-Numba via pip:\n\n```bash\npip install louvain-numba\n```\n\nOr using Poetry:\n\n```bash\npoetry add louvain-numba\n```\n\n## Usage\n\n### Basic Usage\n\n```python\nimport networkx as nx\nimport louvain_numba as lvn\n\n# Create a random graph\nG = nx.random_partition_graph([100, 100, 100], 0.1, 0.01)\n\n# Find the best partition\npartition = lvn.best_partition(G)\nprint("Best partition:", partition)\n\n# Calculate modularity\nmodularity = lvn.modularity(partition, G)\nprint("Modularity:", modularity)\n```\n\n### Specify prefered number of clusters\n\n```python\nimport networkx as nx\nimport louvain_numba as lvn\n\n# Create a random graph\nG = nx.random_partition_graph([100, 100, 100], 0.1, 0.01)\n\n# Find the best partition\npartition = lvn.best_partition(G, n_clusters=(7, 10))\nprint("Best partition:", partition)\n\n# Calculate modularity\nmodularity = lvn.modularity(partition, G)\nprint("Modularity:", modularity)\n```\n\n### Full Hierarchy\n\n```python\nimport networkx as nx\nimport louvain_numba as lvn\n\n# Create a random graph\nG = nx.random_partition_graph([100, 100, 100], 0.1, 0.01)\n\n# Generate full hierarchy of partitions\nfor level, (partition, modularity) in enumerate(lvn.find_partitions(G, return_modularity=True)):\n    print(f"Level {level}:")\n    print("Partition:", partition)\n    print("Modularity:", modularity)\n```\n\n## Contributing\n\nContributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on GitHub.\nLicense\n\nThis project is licensed under the MIT License. See the LICENSE file for details.\n\n## Acknowledgements\n\nThis library was inspired by the cylouvain package and leverages Numba for performance optimization.',
    'author': 'Maixent Chenebaux',
    'author_email': 'max.chbx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
