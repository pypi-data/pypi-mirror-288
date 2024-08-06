import pathlib
import setuptools

setuptools.setup(
    name='jerry_finance_charts_apple',
    version='0.2.0',
    description='A simple python package to run specific actions on a csv file for apple stock prices',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Jerry Osorio",
    license="The Unlicense",
    classifiers=[
        "Topic :: Utilities"
    ],
    python_requires=">=3.10, <3.12",
    install_requires=["pandas>=2.2", "plotly>=5.23"],
    packages=setuptools.find_packages(),
    include_package_data=True
)