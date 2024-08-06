from setuptools import setup, find_packages
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pastesh",
    version="0.1.5",
    author="Wooyoung Han",
    author_email="hanu@a-fin.co.kr",
    description="A Python package for creating encrypted pastes using Paste.sh",
    long_description = long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
