# setup.py
# from setuptools import setup, find_packages
#
# setup(
#     name='ligoauth',
#     version='0.0.7',
#     description='ligo upload mac sdk',
#     packages=find_packages(),
#     python_requires='>=3.6',
# )

from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("ligoauth.ligoauth", ["ligoauth/ligoauth.py"]),
]

setup(
    name='ligoauth',
    version='0.0.7',
    packages=['ligoauth'],
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
