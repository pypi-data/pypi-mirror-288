# setup.py
from setuptools import setup, find_packages
setup(
    name="cmiron-package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="cmiron",
    author_email="cmiron@naver.com",
    description="python-repo-practice",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/cmiron/python-study",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
