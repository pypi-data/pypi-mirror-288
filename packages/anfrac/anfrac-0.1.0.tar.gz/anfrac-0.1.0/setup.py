# setup.py

from setuptools import setup, find_packages

setup(
    name='anfrac',
    version='0.1.0',
    author='Anvai Shrivastava',
    author_email='anvaishrivastava@gmail.com',
    description='A custom Fraction data type library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/anvai0304/anfrac",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
