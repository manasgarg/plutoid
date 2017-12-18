#!/usr/bin/env python3

from setuptools import setup

setup( name="plutoid",
    version = "0.1.3",
    description = "A light weight Python kernel",
    author = "Manas Garg",
    author_email = "manasgarg@gmail.com",
    license = "MIT",
    url = "https://github.com/manasgarg/plutoid",
    packages = ["plutoid"],
    install_requires = ['blinker>=1.4', 'numpy>=1.13.1', 'matplotlib>=2.0.2'],
    long_description = "Plutoid is a light weight Python kernel that can be used for adding code execution capabilities to programming education applications."
)