from distutils.core import setup

setup(
    name='GiiLoto',
    version='0.1',
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
