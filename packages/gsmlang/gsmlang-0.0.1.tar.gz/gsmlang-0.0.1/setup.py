import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsmlang",
    version="0.0.1",
    author="kooperyang",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 2.7"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=2.7",
)