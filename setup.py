from setuptools import setup, find_packages

setup(
    name="McSquirrel",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mcSquirrel=mcSquirrel.__main__:main',
        ],
    },
)
