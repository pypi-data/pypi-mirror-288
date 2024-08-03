from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="UzbekistanWeather",
    version="1.0.6",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Sino",
    author_email="farmonovsino@gmail.com",
    url="https://github.com/sinofarmonovzfkrvjl",
    install_requires=[
        'requests',
        'beautifulsoup4'
    ]
)