import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytrading212",
    version="0.2.7",
    author="HellAmbro",
    author_email="frambrosini1998@gmail.com",
    description="Unofficial Trading212 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HellAmbro/Trading212API",
    packages=setuptools.find_packages(),
    dependencies=[
        'selenium',
        'requests',
        'rich',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
