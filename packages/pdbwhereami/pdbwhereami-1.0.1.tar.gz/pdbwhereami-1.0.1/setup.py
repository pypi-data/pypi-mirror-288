from setuptools import setup

setup(
    name="pdbwhereami",
    version="1.0.1",
    py_modules=["pdbwhereami"],
    install_requires=[
    ],
    author="Bhagavan",
    author_email="bhagavansprasad@gmail.com",
    description="By leveraging `pdbwhereami`, developers can create more robust, maintainable, and easier-to-debug code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bhagavansprasad/pdbwhereami.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)