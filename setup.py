from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Exact Ray Tracing Software '
LONG_DESCRIPTION = 'Exact Ray Tracing Sofware developed for Educational/Professional uses'

setup(
    name="exactraytrace",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Bryce Hirschfeld",
    author_email="cbhirsch859@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Optical Engineers/Students",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)