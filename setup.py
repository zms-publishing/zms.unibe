from setuptools import setup, find_namespace_packages
import os

CLASSIFIERS = [
  'Development Status :: 3 - Alpha',
  'Framework :: Zope :: 5',
  'Programming Language :: Python :: 3',
  'Operating System :: OS Independent',
  'Environment :: Web Environment',
  'Topic :: Internet :: WWW/HTTP :: Site Management',
  'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
  'Intended Audience :: Education',
  'Intended Audience :: Science/Research',
  'Intended Audience :: Customer Service',
  'Intended Audience :: End Users/Desktop',
  'Intended Audience :: Information Technology',
  'License :: OSI Approved :: GNU General Public License (GPL)',
]

setup_path = os.path.dirname(__file__)

setup(
  name                  = 'zms.unibe',
  description           = 'Addons package to extend ZMS for UniBE CMS',
  long_description      = '',
  version               = '0.0.1',
  author                = 'University of Bern, IT Services',
  author_email          = '',
  url                   = '',
  download_url          = '',
  install_requires      = open(os.path.join(setup_path, 'requirements.txt')).readlines(),
  packages              = find_namespace_packages(where='src/', include=['zms.unibe.*']),
  package_dir           = {'': 'src'},
  package_data          = {'': ['*.zcml']},
  classifiers           = CLASSIFIERS,
  include_package_data  = True,
  zip_safe              = False,
  extras_require        = {},
)
