#!/usr/bin/env python
import os
import sys
from setuptools import setup
from setuptools.command.build_py import build_py

class MyBuild(build_py):
    def run(self):
        # Execute the standard build process
        build_py.run(self)
        
        # Add the 'src' directory to the module search path
        root_dir = os.path.abspath(os.path.dirname(__file__))
        sys.path.insert(1, os.path.join(root_dir, "src"))
        
        # Import and use Genkanwadict
        from merumdict import Genkanwadict
        
        # Generate dictionaries if not in dry_run mode
        if not self.dry_run:
            kanwa = Genkanwadict()
            dstdir = os.path.join(self.build_lib, "pymerum", "data")
            kanwa.generate_dictionaries(dstdir)

setup(
    name="pymerum",
    version="0.0.2",  # Specify the version manually
    setup_requires=["setuptools>=42", "setuptools_scm>=8.0.0"],
    cmdclass={"build_py": MyBuild},
    packages=["pymerum"],  # Adjust based on your package structure
    package_dir={"": "src"},  # Source directory
    # other parameters such as author, description, etc.
)
