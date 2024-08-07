from setuptools import setup, find_packages


setup(
    name="image-distillation",
    version="0.1.6",# change it
    description="Python package for image datasets distillations via clustering and grid-based sampling",
    author="Serdar Biçici",
    author_email="serdarbicici1@gmail.com",
    url="https://github.com/serdarbicici-visualstudio/image-distillation",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-learn",
    ],
    license="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    python_requires='>=3.9',
    long_description="Python package for image datasets distillations via clustering and grid-based sampling",
)