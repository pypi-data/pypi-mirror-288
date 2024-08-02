from setuptools import setup, find_packages

with open('README_ChromeAPI.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="chromeAPI",
    version="0.2.1",
    author="Than Tuan Bao",
    author_email="thantuanbao66@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
