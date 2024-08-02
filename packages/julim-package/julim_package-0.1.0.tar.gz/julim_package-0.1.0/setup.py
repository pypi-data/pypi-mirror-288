from setuptools import setup, find_packages
setup(
    name="julim-package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="julim",
    author_email="whizkid00@gmail.com",
    description="공부해",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/koesnuj/python-study",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)