from setuptools import setup, find_packages

setup(
    name='JDKMAN',
    version='0.1.0',
    description='CLI tool for managing multiple JDK versions',
    author='Michael Bui',
    url='https://github.com/michaelbui99/JDKMAN',
    requires=[],
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": ["jdkman=jdkman.__main__:jdkman"]
    }
)
