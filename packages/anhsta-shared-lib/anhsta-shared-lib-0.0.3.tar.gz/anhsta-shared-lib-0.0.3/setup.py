from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize


extensions = [
    Extension(name="testing_module", sources=["./anhsta-shared-lib/testing_module.pyx"]),
]

setup(
    name="anhsta-shared-lib",
    version="0.0.3",
    ext_modules=cythonize(extensions),
    packages=find_packages(),
)