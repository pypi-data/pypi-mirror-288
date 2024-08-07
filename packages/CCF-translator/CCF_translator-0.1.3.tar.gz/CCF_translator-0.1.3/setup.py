from setuptools import setup, find_packages

setup(
    name="CCF_translator",
    version='0.1.3',
    packages=find_packages(),
    license='MIT',
    description='a package to translate data between common coordinate templates',
    package_data={'CCF_translator':["metadata/translation_metadata.csv"]}
)