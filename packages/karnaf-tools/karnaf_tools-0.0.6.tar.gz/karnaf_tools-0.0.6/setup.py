from setuptools import setup, find_packages

setup(
    name="karnaf_tools",
    version="0.0.6",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "matplotlib",
        "argparse",
        "numpy"
    ],
)
