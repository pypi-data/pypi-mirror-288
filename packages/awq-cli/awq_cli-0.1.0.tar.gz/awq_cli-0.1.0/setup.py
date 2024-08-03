"""
A setuptools based setup module.
"""

from setuptools import find_packages, setup

setup(
    name="awq-cli",
    version="0.1.0",
    description="Command-line interface for AutoAWQ",
    long_description="Command-line interface for AutoAWQ",
    url="https://github.com/peakji/awq-cli",
    author="Yichao 'Peak' Ji",
    author_email="pj@ieee.org",
    packages=find_packages(),
    python_requires=">=3.9, <4",
    install_requires=["autoawq", "transformers"],
    entry_points={
        "console_scripts": [
            "awq-cli=awq_cli.__main__:main",
        ],
    },
    keywords="autoawq, awq, llm, quantization",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: GPU",
        "Environment :: GPU :: NVIDIA CUDA",
        "Environment :: GPU :: NVIDIA CUDA :: 11.8",
        "Environment :: GPU :: NVIDIA CUDA :: 12",
        "Environment :: GPU :: NVIDIA CUDA :: 12 :: 12.1",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
