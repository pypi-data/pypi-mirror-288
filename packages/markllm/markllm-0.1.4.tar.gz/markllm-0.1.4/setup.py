from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

# 读取requirements.txt中的依赖项
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="markllm",
    version="0.1.4",
    author="Leyi Pan",
    author_email="panleyi2003@gmail.com",
    description="MarkLLM: An Open-Source Toolkit for LLM Watermarking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/THU-BPM/MarkLLM",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=requirements,  
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
)