from setuptools import find_packages, setup

with open("readme.md", "r") as file:
    long_description = file.read()

setup(
    name="websockethost",
    version="0.0.3",
    description="Web and python socket host",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package=find_packages(),
    url="https://github.com/lamalice20/websockethost",
    author="lamalice20",
    author_email="discord974a@gmail.com",
    install_requires=["vidstream >= 0.0.14", "pyscreeze >= 0.1.30", "pillow >= 10.4.0"],
    python_requires=">=3.12.4",
)