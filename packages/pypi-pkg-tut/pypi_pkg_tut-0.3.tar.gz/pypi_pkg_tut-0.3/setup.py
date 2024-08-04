from setuptools import setup, find_packages

with open("README.md","r") as f:
    description= f.read()

setup(
    name='pypi_pkg_tut',
    version='0.3',
    packages= find_packages(),
    install_requires=[
        #Add dependencies
    ],
    entry_points={
        "console_scripts": [
          "pypi_pkg_tut-hello =  pypi_pkg_tut:hello", 
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
    
)