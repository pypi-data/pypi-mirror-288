from setuptools import setup, find_packages

setup(
    name="aidp",
    version="0.0.1",
    author="AI Data Platform Engineering Team",
    author_email="aidp@sktai.io",
    description="AI Data Platform",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
