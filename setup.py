import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datasetviewer",
    version="0.0.1",
    author="Dolica Akello-Egwel",
    author_email="dolica.akello-egwel@stfc.ac.uk",
    description="A Python tool for viewing n-D datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DMSC-Instrument-Data/dataset_viewer",
    packages=setuptools.find_packages(),
    tests_require=['nose>=1'],
    test_suite='nose.collector',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
