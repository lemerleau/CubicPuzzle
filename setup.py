from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

setup(
    name="cubicgame",
    version="0.0",
    description="High-dimensional Cubical Sliding Puzzle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Miguel, Merleau",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],


    )
