version = '0.0.1'

from setuptools import setup

install_requires = []

setup(
    name = 'marc2bf',
    version = version,
    url = 'http://github.com/kefo/bf2marc',
    author = 'Kevin Ford',
    author_email = 'kefo@3windmills.com',
    license = 'http://www.opensource.org/licenses/bsd-license.php',
    packages = ['marc2bf'],
    install_requires = install_requires,
    description = 'Convert MARC to Bibframe',
    classifiers = [],
    test_suite = 'test',
    include_package_data=True
)
