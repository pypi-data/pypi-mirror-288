from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'My second Python package'
LONG_DESCRIPTION = 'My second Python package with a slightly longer description'


# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="datepack", 
        version=VERSION,
        author="mahesh",
        author_email="maha560270@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package',"Basic Mathamatic Operations"],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
