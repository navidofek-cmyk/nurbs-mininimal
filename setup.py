from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nurbs-curve-minimal",
    version="1.0.0",
    author="Extracted from geomdl",
    description="Minimální projekt pro NURBS křivky",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nurbs-curve-minimal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Žádné externí závislosti - pouze Python stdlib
    ],
)
