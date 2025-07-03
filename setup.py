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
    version               = '1.0.0a1',
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
            'zodburi'               # https://docs.pylonsproject.org/projects/zodburi/en/latest/
        ],
    },
    entry_points          = {
        'console_scripts': [
            'zms2sql-fetch-agendas = zms.unibe.agenda.sqlmodels.__main__:fetch_agendas',
            'zms2sql-fetch-statusmessages = zms.unibe.mobileapp.sqlmodels.__main__:fetch_statusmessages',

            'zms2sql-update-zmssites = zms.unibe.foundation.sqlmodels.__main__:update_zmssites',
            'zms2sql-update-teasers = zms.unibe.teasers.sqlmodels.__main__:update_teasers',
            'zms2sql-update-newsboxes = zms.unibe.announcements.sqlmodels.__main__:update_newsboxes',
            'zms2sql-update-newsevents = zms.unibe.mobileapp.sqlmodels.__main__:update_newsevents',
            'zms2sql-update-servicelinks = zms.unibe.mobileapp.sqlmodels.__main__:update_servicelinks',
            
            'zms2sql-update-mediareleases = zms.unibe.announcements.sqlmodels.__main__:update_mediareleases',
            'zms2sql-update-uniaktuell = zms.unibe.uniaktuell.sqlmodels.__main__:update_uniaktuell',
            
            'zms2sql-update-zmsobjects = zms.unibe.foundation.sqlmodels.__main__:update_zmsobjects',
            'zms2sql-update-datatables = zms.unibe.datatables.sqlmodels.__main__:update_datatables',
            'zms2sql-update-formulator = zms.unibe.formulator.sqlmodels.__main__:update_formulator',
            'zms2sql-update-contacts = zms.unibe.contacts.sqlmodels.__main__:update_contacts',
            'zms2sql-update-layouts = zms.unibe.layouts.sqlmodels.__main__:update_layouts',
        ]
    }

    # cron officehours
    # - fetch-agendas
    # - fetch-statusmessages
    # - update-servicelinks
    # - update-zmssites
    # - update-teasers
    # - update-newsevents
    #
    # cron daily
    # - ... officehours?
    # - update-newsboxes
    # - update-newsevents
    # - update-mediareleases
    # - update-uniaktuell
    #
    # cron weekly
    # - update-zmsobjects
    # - update-datatables
    # - update-formulator
    # - update-contacts
    # - update-layouts
    #
)
