from setuptools import setup, find_packages

setup(
    name='codenrock',
    version='0.94',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'tuspy',
        'argparse',
        'tqdm',
        'zipfile',
    ],
    entry_points={
        'console_scripts': [
            'codenrock=codenrock.cli:main',
        ],
    },
)
