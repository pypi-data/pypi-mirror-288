from setuptools import setup, find_packages

setup(
    name='pypi_pkg_tut',
    version='0.2',
    packages= find_packages(),
    install_requires=[
        #Add dependencies
    ],
    entry_points={
        "console_scripts": [
          "pypi_pkg_tut-hello =  pypi_pkg_tut:hello", 
        ],
    }
)