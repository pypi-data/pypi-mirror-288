# setup.py
from setuptools import setup, find_packages

setup(
    name='text_to_ascii',
    version='0.2',
    url="https://github.com/noahprero/text-to-ascii",
    author="Noah Prero",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.10.0.84",
        "numpy>=2.0.1"
    ],
    entry_points={
        "console_scripts": [
            "text-to-ascii = text_to_ascii:main",
        ]
    }
)
