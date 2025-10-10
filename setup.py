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
    description           = 'Addons package for ZMS at UniBE',
    long_description      = 'Python-based extensions for and integrations with the ZMS publishing system',
    version               = '1.2.0',
    author                = 'University of Bern, IT Services',
    author_email          = '',
    url                   = 'https://github.com/idasm-unibe-ch/zms-addons',
    download_url          = 'https://github.com/idasm-unibe-ch/zms-addons/releases',
    install_requires      = open(os.path.join(setup_path, 'requirements.txt')).readlines(),
    packages              = find_namespace_packages(where='src/', include=['zms.unibe']),
    package_dir           = {'': 'src'},
    package_data          = {'': ['*.zcml']},
    classifiers           = CLASSIFIERS,
    include_package_data  = True,
    zip_safe              = False,
    extras_require        = {
        'fastapi': [
            'FastAPI',              # https://fastapi.tiangolo.com
            'uvicorn[standard]',    # https://www.uvicorn.org
        ],
    },
    entry_points          = {
        'console_scripts': [
            'zms2sql = zms.unibe.utils.zms2sql.cli:main'
        ]
    }
)
