from setuptools import setup, find_packages

setup(
    name="chromeAPI",
    version="0.2.0",
    author="Than Tuan Bao",
    author_email="thantuanbao66@gmail.com",
    long_description=open('README.md').read(),
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
