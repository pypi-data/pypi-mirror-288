from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Python SQL Manager'
LONG_DESCRIPTION = 'Python SQL Manager based on SQLModel'

setup(
    name="asm-sql-python-crud", 
    version=VERSION,
    author="Alberto Sanmartin Martinez",
    author_email="<albertosanmartinmartinez@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
      
    ],
    
    keywords=[
        'python',
        'sql'
    ],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)