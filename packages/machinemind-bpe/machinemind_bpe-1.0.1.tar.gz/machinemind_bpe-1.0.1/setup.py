from setuptools import setup, find_packages

setup(
    name="machinemind_bpe",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.1.0",
        "torch>=1.7.0",
        "tqdm>=4.0.0",
        "regex>=1.1.1"
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="A Byte Pair Encoding (BPE) tokenizer package for CPU and GPU.",
    author="Javokhir",
    author_email="machinemind60@gmail.com",
    url="https://github.com/machineminduzb_v2/bpe_tokenizer",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
