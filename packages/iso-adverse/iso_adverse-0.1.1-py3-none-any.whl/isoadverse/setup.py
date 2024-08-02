from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iso-adverse",
    version="0.1.1",
    author="Jazmia Henry",
    author_email="isojaz@isoai.co",
    description="This package is designed to simulate adversarial on pre-trained language models (pre-LLM models)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iso-ai/isoadverse",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torch>=1.7.0",
        "transformers>=4.0.0",
    ],
    license="Apache License 2.0",
)