from setuptools import setup, find_packages
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')
with open(README, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="compairer",
    version="0.1.0",
    author="Joel Yisrael",
    author_email="joel@sss.bot",  # Changed from authorEmail
    description="A versatile comparison library for Python",
    long_description=long_description,  # Changed from longDescription
    long_description_content_type="text/markdown",  # Changed from longDescriptionContentType
    url="https://github.com/schizoprada/compairer",
    package_dir={"": "src"},  # Changed from packageDir
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Changed from pythonRequires
    install_requires=[  # Changed from installRequires
        "numpy",
        "fuzzywuzzy",
    ],
)
