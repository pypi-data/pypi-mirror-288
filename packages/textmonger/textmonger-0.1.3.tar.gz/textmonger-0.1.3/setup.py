from setuptools import setup, find_packages
import os
from setuptools.command.install import install

def install_spacy_model():
    os.system('python -m spacy download en_core_web_sm')

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        install_spacy_model()

setup(
    name="textmonger",
    version="0.1.3",
    author="Sahil Garje",
    author_email="sahilgarje@gmail.com",
    description="A text analysis tool with readability, power word analysis, and NER visualization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oceanthunder/TheTextMonger",
    packages=find_packages(),
    install_requires=[
        "spacy",
        "pyfiglet",
        "textstat",
        "pytest",
        "tabulate"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        'textmonger': ['power_words.csv'],
    },
    entry_points={
        'console_scripts': [
            'textmonger=textmonger.project:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
