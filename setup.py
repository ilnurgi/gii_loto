import setuptools

setuptools.setup(
    name='gii_loto',
    version='0.3',
    author='ilnurgi',
    author_email='ilnurgi@mail.ru',
    url='http://ilnurgi.ru',
    packages=setuptools.find_packages(),
    # package_dir={
    #     '': 'src'
    # },
    entry_points={
        'console_scripts': [
            'gii_loto = gii_loto.app:main'
        ]
    }
)
