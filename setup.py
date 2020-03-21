from setuptools import setup, find_packages

setup(
    name='gii_loto',
    version='0.5',
    author='ilnurgi',
    author_email='ilnurgi@mail.ru',
    url='http://ilnurgi.ru',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'pyyaml',
        'bs4',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'gii_loto = gii_loto.app:main'
        ]
    }
)
