from setuptools import setup

setup(
    name='PMAR_Breakdowns',
    version='1.9',
    py_modules=['PMAR_Breakdowns'],
    install_requires=[
        'pandas',
        'matplotlib',
        'numpy'
    ],
    author='Timothy Colledge',
    author_email='timothy.colledge@invesco.com',
    description='This Library serves as a support file for IVZ python scipts. It contains functions and classes that are utilized in data processing for PMAR FI analytics.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
