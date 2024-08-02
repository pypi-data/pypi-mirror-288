from setuptools import find_packages, setup

# To install the library, run the following:
#
# python setup.py install
#

with open("README.md") as f:
    long_description = f.read()

version = "0.14.0"

setup(
    name="shaped",
    version=version,
    author="Shaped Team",
    author_email="support@shaped.ai",
    url="https://github.com/shaped-ai/shaped-cli",
    description="CLI and SDK tools for interacting with the Shaped API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["shaped-ai"],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    packages=find_packages(
        where="sdk/python",
        include=["shaped*"],
        exclude=["sdk/python/tests"],
    ),
    package_dir={'': 'sdk/python'},
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        "typer>=0.7.0",
        "requests>=2.28.1",
        "pydantic>=2.8.2",
        "pyyaml>=6.0",
        "pyarrow==11.0.0",
        "pandas==1.5.3",
        "tqdm==4.65.0",
        "s3fs==0.4.2",
        "fsspec==2023.5.0",
        "numpy==1.26.4",
        "urllib3 >= 1.25.3, < 2.1.0",
        "python-dateutil",
        "typing-extensions >= 4.7.1",
        "pytest==6.2.5",
        "pytest-mock==3.14.0",
    ],
    # TODO(Ben SHA-1977): Investigate Python 3.12 support.
    python_requires=">=3.8, <3.12",
    entry_points={"console_scripts": ["shaped=shaped.cli.shaped_cli:app"]},
    test_suite="sdk.python.tests",
)
