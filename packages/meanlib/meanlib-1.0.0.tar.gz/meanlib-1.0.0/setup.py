from setuptools import setup, find_packages

setup(
    name="meanlib",
    version="1.0.0",
    author="Tobia Petrolini",
    description="A Python package for calculating simple and weighted means, featuring classes for dynamic updates and sliding window functionality.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PinkPantherPC/meanlib.git",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.15.0",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3.7',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'meanlib = meanlib.__main__:main',
        ],
    }
)
