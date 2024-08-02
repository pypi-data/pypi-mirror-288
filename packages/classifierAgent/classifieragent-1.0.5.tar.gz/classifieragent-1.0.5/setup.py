__author__ = "Adnan Karol"
__version__ = "1.0.4"
__maintainer__ = "Adnan Karol"
__email__ = "adnanmushtaq5@gmail.com"
__status__ = "PROD"

# Import Dependencies
from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r") as file:
    long_description = file.read()

# Read dependencies from requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

setup(
    name='classifierAgent',
    version='1.0.5',  # Updated version number
    description='A Python package for performing classification on datasets in CSV or Excel format.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/adnanmushtaq1996/ML-Classifier-Python-Package',
    author='Adnan Karol',
    author_email='adnanmushtaq5@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'machine learning', 'classification', 'random forest', 'xgboost', 
        'svm', 'logistic regression', 'naive bayes', 'knn', 'decision tree'
    ],
    python_requires='>=3.10',
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'classifierAgent=classifierAgent.cli:main',
        ],
    },
    project_urls={
        'Documentation': 'https://github.com/adnanmushtaq1996/ML-Classifier-Python-Package',
        'Source': 'https://github.com/adnanmushtaq1996/ML-Classifier-Python-Package',
        'Tracker': 'https://github.com/adnanmushtaq1996/ML-Classifier-Python-Package/issues',
    },
)
