from distutils.core import setup

setup(
    name='gii_loto',
    version='0.2',
    author='ilnurgi',
    author_email='ilnurgi@mail.ru',
    url='http://ilnurgi.ru',
    package_dir={
        '': 'src'
    },
    entry_points={
        'console_scripts': [
            'gii_loto = gii_loto.app:main'
        ]
    }
)
