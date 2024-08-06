from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ext_modules = cythonize(Extension(
    "Aligner",
    sources=["src/c_align.pyx", "src/align.cpp", "src/AlignTools.cpp"],
    language="c++",
    library_dirs=['lib'],
    include_dirs=['src', numpy.get_include()],
    libraries=[],
    extra_compile_args=['-std=c++14'],
))

setup(
    name='weighted_align',
    version='1.1',
    description='A tool for aligning DNA or marker seq.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Junyi He',
    author_email='guilitianya@126.com',
    url='https://github.com/CycloneSEQ-Bioinformatics/Weighted_Align.git',
    packages=find_packages(),
    ext_modules=ext_modules,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
    setup_requires=[
        'cython',
    ],
)