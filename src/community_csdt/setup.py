import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pyramid_beaker',
    'pycrypto==2.3',
    'mysql-python',
    'beautifulsoup',
    'recaptcha-client',
    'tinyurl',
    'transaction',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'WebError'
    ]

setup(name='community_csdt',
      version='0.0',
      description='community_csdt',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="community_csdt",
      entry_points = """\
      [paste.app_factory]
      main = community_csdt:main
      """,
      )

