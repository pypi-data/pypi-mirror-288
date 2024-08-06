from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cdxj_util",
    version="1.0.0",
    author="r74tech",
    author_email="r74tech@gmail.com",
    description="A utility library for working with CDXJ files",
    keywords="cdxj openwayback wayback",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r74tech/cdxj-util",
    packages=find_packages(exclude=["tests*", "examples*", "data*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiofiles",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
        ],
    },
)
