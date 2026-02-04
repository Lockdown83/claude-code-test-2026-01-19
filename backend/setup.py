"""Setup configuration for VC Dashboard CLI."""
from setuptools import setup, find_packages
from pathlib import Path


# Read README if it exists
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''


setup(
    name='vc-dashboard-cli',
    version='1.0.0',
    py_modules=['cli', 'cli_config', 'cli_formatters', 'cli_api'],
    install_requires=[
        'click>=8.0.0',
        'requests>=2.28.0',
        'rich>=13.0.0',
    ],
    entry_points={
        'console_scripts': [
            'vc-dashboard=cli:cli',
        ],
    },
    author='Andrew DiMaulo',
    description='Command-line interface for VC Dashboard - Track jobs and dealflow from the terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/vc-dashboard',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Office/Business',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    keywords='vc venture-capital jobs dealflow cli dashboard',
)
