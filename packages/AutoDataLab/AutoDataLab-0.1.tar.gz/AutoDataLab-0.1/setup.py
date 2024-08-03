from setuptools import setup, find_packages

setup(
    name = 'AutoDataLab',
    version = '0.1',
    long_description_content_type="text/markdown",
    long_description='README',
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