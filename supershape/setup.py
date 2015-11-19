from distutils.core import setup, Extension

cSuperformula = Extension("cSuperformula",
                          sources = ["superformula.c"] )

setup (name = "supershape",
       version = "1.0",
       author = "Frederik De Bleser. Superformula by Johan Gielis.",
       description = "Library for calculating the superformula.",
       ext_modules = [cSuperformula])