<p align="center">
    <a href=""><img src="./docs/source/_static/ift_global_banner.png" alt="IFTGBanner-BigData-IFT"></a>
</p>
<p align="center">
    <em>IFT Global Python Package</em>
</p>

|||
|--------|------|
|**Build**|![Build Status](https://github.com/iftucl/ift_global/actions/workflows/build.yml/badge.svg)|
|**Coverage**|![Coverage](https://github.com/iftucl/ift_global/actions/workflows/test.yml/badge.svg)|
|**Linting**|![Linters](https://github.com/iftucl/ift_global/actions/workflows/linting.yml/badge.svg)|
|**Vulnerability Scan**|![Vulnerability](https://github.com/iftucl/ift_global/actions/workflows/vulnerability-scan.yml/badge.svg)|

# ift_global

**IFT Global** is a python package that provides basic abstraction functionalities used for python scripting in the Big Data in Quantitative Finance module @uclift.

## Main Features

- business dates : abstraction to retrive previous business dates.
- connectors : client abstraction for file system on MinIO.
- database : client abstraction to interface with Postgresql.
- email : email client abstraction to send automated email messages.

## How to get

The artifacts of this repository are not yet pushed to pypi. However, the .whl and tar files are available for download on the Build Pipeline within this repo. As the package has not yet reached a stable state we won't publish to pypi.