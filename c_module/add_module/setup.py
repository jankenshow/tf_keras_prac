from distutils.core import setup, Extension

setup(name = "add_module",
    version = "1.0.0",
    ext_modules = [Extension("add_module", ["add_module.cpp"])]
    )