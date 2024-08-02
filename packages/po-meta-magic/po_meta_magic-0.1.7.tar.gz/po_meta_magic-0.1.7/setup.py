from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="po_meta_magic",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[
        'pillow',
        'fuzzywuzzy',
        'python-dateutil',
        'pytesseract',
    ],
    author="Muhammad Abuzar",
    author_email="abuzar9658@gmail.com",
    description="A Python package for extracting and processing text from images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/po_meta_magic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
