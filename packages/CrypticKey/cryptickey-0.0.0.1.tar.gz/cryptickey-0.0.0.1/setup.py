from setuptools import setup, find_packages

setup(
    name="CrypticKey",
    version="0.0.0.1",
    packages=find_packages(),
    description="A custom module that generates a random password for you.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sidharth (NINJA)",
    author_email="sidharthsnair357@gmail.com",
    url="https://github.com/NINJAGAMING107/CrypticKey",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
