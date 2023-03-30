from setuptools import setup, find_packages

setup(
    name='JDKMAN',
    version='0.2.0',
    description='CLI tool for managing multiple JDK versions',
    author='Michael Bui',
    url='https://github.com/michaelbui99/JDKMAN',
    requires=[
        'beautifulsoup4',
        'click',
        'lxml',
        'requests',
        'selenium',
        'webdriver_manager'
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": ["jdkman=jdkman.__main__:jdkman"]
    }
)
