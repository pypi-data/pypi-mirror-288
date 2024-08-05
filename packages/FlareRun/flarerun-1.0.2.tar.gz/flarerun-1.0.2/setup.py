from setuptools import setup, find_packages

setup(
    name="FlareRun",
    version="1.0.2",
    author="Aryan Chander",
    author_email="aryanchander5@gmail.com",
    description="A Python library for interacting with FlareRun's trading APIs",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://flarerun.online",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
