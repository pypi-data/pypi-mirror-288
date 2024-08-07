# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlstac']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.4',
 'pandas>=2.1.4',
 'rasterio>=1.3.10',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'mlstac',
    'version': '0.1.1',
    'description': 'A Common Language for EO Machine Learning Data',
    'long_description': '# mlstac\n\n[![Release](https://img.shields.io/github/v/release/csaybar/mlstac)](https://img.shields.io/github/v/release/csaybar/mlstac)\n[![Build status](https://img.shields.io/github/actions/workflow/status/csaybar/mlstac/main.yml?branch=main)](https://github.com/csaybar/mlstac/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/csaybar/mlstac/branch/main/graph/badge.svg)](https://codecov.io/gh/csaybar/mlstac)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/csaybar/mlstac)](https://img.shields.io/github/commit-activity/m/csaybar/mlstac)\n[![License](https://img.shields.io/github/license/csaybar/mlstac)](https://img.shields.io/github/license/csaybar/mlstac)\n\nA Common Language for EO Machine Learning Data\n\n- **Github repository**: <https://github.com/csaybar/mlstac/>\n- **Documentation** <https://csaybar.github.io/mlstac/>\n\n## Getting started with your project\n\nFirst, create a repository on GitHub with the same name as this project, and then run the following commands:\n\n```bash\ngit init -b main\ngit add .\ngit commit -m "init commit"\ngit remote add origin git@github.com:csaybar/mlstac.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with\n\n```bash\nmake install\n```\n\nYou are now ready to start development on your project!\nThe CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/csaybar/mlstac/settings/secrets/actions/new).\n- Create a [new release](https://github.com/csaybar/mlstac/releases/new) on Github.\n- Create a new tag in the form `*.*.*`.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Cesar Aybar',
    'author_email': 'fcesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/csaybar/mlstac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
