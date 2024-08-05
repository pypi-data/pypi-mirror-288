from setuptools import setup, find_packages

setup(
    name="StatGrit",
    version="0.1.1",
    packages=find_packages(),
    description="This a custom module for tracking local game scores which are modfied manually.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sidharth (NINJA)",
    author_email="sidharthsnair357@gmail.com",
    url="https://github.com/NINJAGAMING107/statgrit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
