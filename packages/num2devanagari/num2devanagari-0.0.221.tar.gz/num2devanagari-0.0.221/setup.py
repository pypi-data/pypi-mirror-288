
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '0.0.221'
DESCRIPTION = 'Convert numbers to Devanagari words'
LONG_DESCRIPTION = 'A package to convert numbers to Devanagari words'

# Setting up
setup(
    name="num2devanagari",
    version=VERSION,
    author="Aananda-Giri",
    author_email="<aanandaprashadgiri@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)


# setup(
#     name='',
#     version='1.0',
    
#     install_requires=[],
#     author='Aananda Giri',
#     author_email='aanandaprashadgiri@gmail.com',
#     description='Convert numbers to Devanagari words',
#     long_description='A package to convert numbers to Devanagari words',
#     keywords='devanagari numbers conversion',
#     classifiers=[
#         'Development Status :: 5 - Production/Stable',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7',
#         'Programming Language :: Python :: 3.8',
#     ],
# )






