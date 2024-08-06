from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'AutoDataLab',
    version = '0.1.1',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages = find_packages(),
    install_requires = [
        # add dependencies here 
        # e.g. 'numpy>=1.11.1'
    ],
    
    entry_points = {
        "console_scripts": [
            "AutoDataLab = AutoDataLab:hello",
        ],
    },
)