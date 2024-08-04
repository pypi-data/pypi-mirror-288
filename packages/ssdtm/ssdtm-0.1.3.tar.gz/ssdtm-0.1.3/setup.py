import pathlib
import setuptools
#from setuptools import setup, find_packages

setuptools.setup(
    name='ssdtm',
    version='0.1.3',
    author='Akshay Chougule',
    author_email='akshay6023@gmail.com',
    description='A package that can generate low-fidelity synthetic CDISC SDTM data based on intelligent sequence generators',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    license='MIT',
    project_urls={
        "source":"https://github.com/AksChougule/gen-sdtm",
        },
    classifiers=[
            "Intended Audience :: Science/Research",
            "Development Status :: 2 - Pre-Alpha",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11"
        ],
    install_requires=["pandas","numpy","datetime"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
