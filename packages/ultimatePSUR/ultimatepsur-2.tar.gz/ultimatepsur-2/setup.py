from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ultimatePSUR",
    version="2",
    author="Lixense",
    author_email="lixlix870@gmail.com",
    description="A powerful proxy scraper, updater, and rotator library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lixense/ultimatePSUR",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "requests",
    ],
)