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
from setuptools.command.build_ext import build_ext
import os

# Define the extension module
extensions = [
    Extension("ligoauth.ligoauth", ["ligoauth/ligoauth.py"]),
]


class BuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        # Remove the original source files
        for ext in self.extensions:
            source = ext.sources[0]
            if os.path.exists(source):
                os.remove(source)


setup(
    name='ligoauth',
    version='0.0.8',
    packages=['ligoauth'],
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
    include_package_data=True,
    description='ligoauth sdk',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    cmdclass={'build_ext': BuildExt},
)
