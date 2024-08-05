from setuptools import setup, find_packages


setup(
    name='pwdf',
    version='0.0.1',
    description='A terminal command (Python module) to get the path of a file (pwd for files instead of directories).',
    url='https://github.com/rynstwrt/pwdf',
    author='Ryan Stewart',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pwdf=pwdf.pwdf:run'
        ]
    },
)
