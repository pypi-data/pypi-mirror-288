from setuptools import setup, find_packages

setup(
    name="trialpack",
    version="1.0.1",
    packages=find_packages(),
    description="A custom 'this' module with programming principles and poem",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sidharth (NINJA)",
    author_email="sidharthsnair357@gmail.com",
    url="https://github.com/NINJAGAMING107/trialpack",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
