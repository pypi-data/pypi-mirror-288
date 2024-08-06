from os import path as os_path

from loguru import logger
from setuptools import find_packages
from setuptools import setup

PACKAGE_NAME = 'zf-xanthus'
AUTHOR_NAME = 'Zeff Muks'
AUTHOR_EMAIL = 'zeffmuks@gmail.com'


def read_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), 'xanthus', 'version.py')
    with open(version_file) as file:
        exec(file.read())
    version = locals()['__version__']
    logger.debug(f"Building {PACKAGE_NAME} v{version}")
    return version


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


setup(
    name=PACKAGE_NAME,
    version=read_version(),
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='xanthus generates weekly updates from X bookmarks',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=get_requirements(),
    packages=find_packages(
        exclude=['venv', 'venv.*']
    ),
    package_data={
        'xanthus': ['*.json', '*.yaml', '*.yml', '*.txt'],
    },
    entry_points={
        'console_scripts': [
            'xanthus=xanthus.__main__:run_main'
        ]
    },
    license='Proprietary',
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
