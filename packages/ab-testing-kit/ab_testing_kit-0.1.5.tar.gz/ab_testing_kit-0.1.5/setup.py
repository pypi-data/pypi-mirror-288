"""To build custom package"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the content of your README file
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='ab_testing_kit',
    version='0.1.5',
    description="Useful functions for A/B testing and data exploration",
    author='Oamen Modupe',
    author_email='oamenmodupe@gmail.com',
    packages = ['ab_testing_kit.exploration', 
                'ab_testing_kit.data_splitting',
                'ab_testing_kit.testing'],
    install_requires=[
        'numpy==1.23.5',
        'pandas==1.5.3',
        'pillow==10.4.0',
        'seaborn==0.12.2',
        'packaging==23.1',
        'pyarrow==15.0.2',
        'matplotlib==3.7'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
