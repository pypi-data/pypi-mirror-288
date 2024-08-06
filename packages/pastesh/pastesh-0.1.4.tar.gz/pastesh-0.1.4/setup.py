from setuptools import setup, find_packages

setup(
    name="pastesh",
    version="0.1.4",
    author="Wooyoung Han",
    author_email="hanu@a-fin.co.kr",
    description="A Python package for creating encrypted pastes using Paste.sh",
    # long_description=open("README.md").read(),
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
