from setuptools import setup, find_packages
from pathlib import Path


long_description = (Path(__file__).parent / "README.md").read_text()


setup(
    name='pwdf',
    version='1.0.1',
    description='A terminal command (Python module) to get the path of a file (pwd for files instead of directories).',
    url='https://github.com/rynstwrt/pwdf',
    author='Ryan Stewart',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pwdf=pwdf.pwdf:run'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
