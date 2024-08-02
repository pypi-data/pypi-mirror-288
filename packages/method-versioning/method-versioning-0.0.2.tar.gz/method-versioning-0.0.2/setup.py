from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="method-versioning",
    version="0.0.2",
    author="Sanghun Lee",
    author_email="nrhys2005@gmail.com",
    description="Method versioning package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nrhys2005/method-versioning",
    packages=find_packages(include=['method_versioning', 'method_versioning.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
)
