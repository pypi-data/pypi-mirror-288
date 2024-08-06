from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="solv_ai",
    version="0.1.0",
    author="CloudSolv AI",
    author_email="eric@cloudsolv.co",
    description="A high-performance AI model optimization library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CloudSolv-AI/solv_ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.18.0,<2.0.0",
        "torch>=1.6.0,<2.5.0",
        "torchvision>=0.7.0,<1.0.0"
    ],
)