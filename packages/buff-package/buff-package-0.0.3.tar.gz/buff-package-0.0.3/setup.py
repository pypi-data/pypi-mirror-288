# setup.py

from setuptools import setup, find_packages

setup(
    name="buff-package",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[],
    author="buff",
    author_email="buff@kakao.com",
    description="Practice Package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/buff91/python-practice",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
