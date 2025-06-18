from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ip-changer",
    version="1.0.0",
    description="A command-line tool for changing IP addresses on Windows and Linux systems",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/ip-changer",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Topic :: System :: Networking",
        "Topic :: Utilities"
    ],
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
        "netifaces>=0.11.0",
    ],
    extras_require={
        'windows': ['pywin32>=306'],
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'mypy>=1.5.1',
            'flake8>=6.1.0',
        ],
        'docs': [
            'mkdocs>=1.5.2',
            'mkdocs-material>=9.2.3',
        ]
    },
    entry_points={
        'console_scripts': [
            'ipchanger=ipchanger.cli:main',
            'ip-changer=ipchanger.cli:main',  # Alternative command name
        ],
    },
    python_requires='>=3.6',
    keywords='ip networking cli windows linux network-administration',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/ip-changer/issues',
        'Source': 'https://github.com/yourusername/ip-changer',
    },
)
