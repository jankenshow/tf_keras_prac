from distutils.core import setup, Extension

setup(name = "hello_module", 
    version = "1.0.0",
    ext_modules = [Extension("hello_module", ["hello_module.cpp"])])