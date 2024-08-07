from setuptools import setup, find_packages

setup(
    name="haruko",
    version="1.0.14",
    packages=['haruko'],
    entry_points={
        'console_scripts': [
            'haruko=haruko.haruko:main',
        ],
    },
    author="Veilwr4ith",
    author_email="hacktheveil@gmail.com",
    description="An Advanced Password Wordlist Generator for Brute-Force an Dictionary Attacks",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/veilwr4ith/Haruko",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
