from setuptools import setup, find_packages

setup(
    name='shape-challenge',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'numpy',
        'pytest',
        'joblib',
    ],
    entry_points={
        'console_scripts': [
            'shape-challenge = main:main',  # Define o comando para execução via terminal
        ],
    },
)
