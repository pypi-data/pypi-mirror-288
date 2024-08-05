from setuptools import find_packages, setup

setup(
    name="credold",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["boto3"],
    author="Akira Kobori",
    author_email="private.beats@gmail.com",
    description="A package for managing credentials",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/koboriakira/credold",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
