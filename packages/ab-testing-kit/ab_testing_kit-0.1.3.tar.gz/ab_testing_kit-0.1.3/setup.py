"""To build custom package"""
from setuptools import setup

setup(
    name = 'ab_testing_kit',
    version = '0.1.3',
    description= "Useful functions for ab testing and data exploration",
    author='oamenmodupe@gmail',
    packages = ['ab_testing_kit.exploration', 
                'ab_testing_kit.data_splitting',
                'ab_testing_kit.testing'],
    install_requires = ['numpy==1.23.5', 
                        'pandas==1.5.3',
                        'pillow==10.4.0',
                        'seaborn==0.12.2','packaging==23.1','pyarrow==15.0.2',
                        'matplotlib==3.7'
                        ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.10',
)