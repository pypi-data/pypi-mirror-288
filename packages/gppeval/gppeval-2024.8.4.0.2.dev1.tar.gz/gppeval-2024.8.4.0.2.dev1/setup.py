import os
from setuptools import setup, find_packages

__version_info__ = (2024, 8, 4, 0, 2, 'dev1')
__version__ = '.'.join(map(str, __version_info__))
__author__ = 'Carlos O. POCASANGRE JIMENEZ'
__description__ = 'Geothermal Power Potential assessment'
__url__ = 'https://github.com/cpocasangre/gppeval'
__module_name__ = 'gppeval'
__author_email__ = 'carlos.pocasangre@ues.edu.sv'
__license__ = 'MIT License'
__status__ = 'Development release'

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

readme = 'README.rst'

setup(
    name=__module_name__,
    version=__version__,
    description=__description__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,

    long_description=read(readme),
    packages=find_packages(exclude=['test*']),
    
    keywords=["monte carlo",
              "latin hypercube",
              "geothermal power potential",
              "volumetric method",
              "geothermal reservoir"],
    install_requires=['numpy', 
                      'scipy', 
                      'matplotlib', 
                      'mcerp', 
                      'beautifultable', 
                      'iapws'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Environment :: MacOS X',
                 'Environment :: X11 Applications',
                 'Environment :: Win32 (MS Windows)',
                 'Natural Language :: English',
                 'Operating System :: Microsoft',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: MacOS :: MacOS X',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.8'],
    zip_safe=False,
)
