# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipset_c']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.8.0,<2.0.0', 'setuptools>=70.0.0,<71.0.0']

setup_kwargs = {
    'name': 'ipset_c',
    'version': '0.1.0.dev2',
    'description': 'IPSet written in C',
    'long_description': '# ipset_c\n\nIPSet is written in C.\nRuns on Windows and Linux.\nTens of times faster than pure Python netaddr.IPSet.\nOnly for IPv4. Not picklable.\n\n\n```\npip install ipset_c\n```\n\n```\nfrom ipset_c import IPSet\na = IPSet([\'12.12.12.0/25\', \'12.12.12.128/25\'])\na.getCidrs()  # [\'12.12.12.0/24\']\na.addCidr(\'8.8.8.8/30\')\na.getCidrs()  # [\'8.8.8.8/30\', \'12.12.12.0/24\']\nb = IPSet([\'12.12.12.0/25\'])\na.isSubset(b)  # False\na.isSuperset(b)  # True\na == b  # False\na <= b  # False\na >= b  # True\na.isContainsCidr("12.12.0.0/16")  # False\na.isIntersectsCidr("12.12.0.0/16")  # True\nb.addCidr(\'4.4.4.4/32\')\na.getCidrs()  # [\'8.8.8.8/30\', \'12.12.12.0/24\']\nb.getCidrs()  # [\'4.4.4.4/32\', \'12.12.12.0/25\']\nc = a & b\nc.getCidrs()  # [\'12.12.12.0/25\']\nc = a | b\nc.getCidrs()  # [\'4.4.4.4/32\', \'8.8.8.8/30\', \'12.12.12.0/24\']\nc = a - b\nc.getCidrs()  # [\'8.8.8.8/30\', \'12.12.12.128/25\']\na.removeCidr(\'8.8.8.8/30\')\na.getCidrs()  # [\'12.12.12.0/24\']\nlen(a)  # 256\nc = a.copy()\nbool(IPSet([]))  # False\n```\n',
    'author': 'glowlex',
    'author_email': 'antonioavocado777@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
