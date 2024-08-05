#!/usr/bin/env python

####+BEGIN: bx:dblock:global:file-insert :mode python :file "/bisos/apps/defaults/begin/templates/purposed/pyModule/python/commonSetupCode.py"

import setuptools
import re
import inspect
import pathlib

def pkgName():
    """ From this eg., filepath=.../bisos-pip/PkgName/py3/setup.py, extract PkgName. """
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    grandMother = pathlib.Path(filename).resolve().parent.parent.name
    return f"bisos.{grandMother}"

def description():
    """ Extract title from ./README.org which is expected to have a title: line. """
    with open('./README.org') as file:
        while line := file.readline():
            if match := re.search(r'^#\+title: (.*)',  line.rstrip()):
                return match.group(1)
            return "MISSING TITLE in ./README.org"

def longDescription():
    """ Convert README.org to README.rst. """
    try:
        import pypandoc
    except ImportError:
        result = "warning: pypandoc module not found, could not convert to RST"
        return result
    return pypandoc.convert_file('README.org', 'rst')


####+END:

####+BEGIN: b:py3:pypi/nextVersion :increment 0.01

def pkgVersion():
    pypiUploadVerFile = pathlib.Path('./pypiUploadVer')
    if pypiUploadVerFile.is_file() :
        return '0.17'
    else:
        return '0.16'

####+END:

####+BEGINNOT: b:py3:pypi/requires :extras ()

requires = [
    "blee",
    "blee.icmPlayer",
    "bisos",
    "bisos.b",
    "bisos.common",
]
####+END:

####+BEGIN: b:py3:pypi/scripts :comment ""

scripts = [
'./bin/bx-bases',
'./bin/bx-isoSrBases.py',
'./bin/bx-pip',
]
####+END:

#
# Data files are specified in ./MANIFEST.in as:
# recursive-include unisos/marme-base *
# recursive-include unisos/marme-config *
#

data_files = [
]

####+BEGIN: bx:dblock:global:file-insert :mode python :file "/bisos/apps/defaults/begin/templates/purposed/pyModule/python/commonSetuptools.py"

setuptools.setup(
    name=pkgName(),
    version=pkgVersion(),
    packages=setuptools.find_packages(),
    scripts=scripts,
    #data_files=data_files,
    include_package_data=True,
    zip_safe=False,
    author='Mohsen Banan',
    author_email='libre@mohsen.1.banan.byname.net',
    maintainer='Mohsen Banan',
    maintainer_email='libre@mohsen.1.banan.byname.net',
    url='http://www.by-star.net/PLPC/180047',
    license='AGPL',
    description=description(),
    long_description=longDescription(),
    download_url='http://www.by-star.net/PLPC/180047',
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )

####+END:
