from setuptools import setup, find_packages

setup(
    name='movies',
    version='0.0.0',
    description='Training project that recommends movies',
    url='https://github.com/Starstaub/movies',
    author='Starstaub',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=['peppercorn'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    include_package_data=True,
)
