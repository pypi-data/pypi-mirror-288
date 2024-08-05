# setup.py
from setuptools import setup, find_packages
setup(
    name="new0325-package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="leehyunho",
    author_email="dae461@nate.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/mypackage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
