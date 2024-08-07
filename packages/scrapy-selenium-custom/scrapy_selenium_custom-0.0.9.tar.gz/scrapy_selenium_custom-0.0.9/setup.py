"""This module contains the packaging routine for the pybook package"""

from setuptools import setup, find_packages
try:
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    # It is quick hack to support pip 10 that has changed its internal
    # structure of the modules.
    try:
        from pip._internal.download import PipSession
        from pip._internal.req.req_file import parse_requirements
    except ModuleNotFoundError:
        pass  # will catch NameError below.. part above doesn't work with Python 3.11+


def get_requirements(source):
    """Get the requirements from the given ``source``

    Parameters
    ----------
    source: str
        The filename containing the requirements

    """

    try:
        install_reqs = parse_requirements(filename=source, session=PipSession())
        return [str(ir.req) for ir in install_reqs]
    except NameError:  # no idea how to fix this properly
        return [
            'scrapy >= 1.0.0',
            'selenium >= 4.1.0',
            "webdriver-manager >= 4.0.2",
        ]


setup(
    packages=find_packages(),
    install_requires=get_requirements('requirements/requirements.txt')
)
