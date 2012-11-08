from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='gites.skin',
      version=version,
      description="An installable theme for Plone 3.0",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone theme',
      author='Affinitic',
      author_email='info@affinitic.be',
      url='http://svn.affinitic.be/plone/gites/gites.skin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gites'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'gites.core',
          'zc.table',
          'collective.captcha',
          'Products.LocalFS',
          'zc.datetimewidget',
          'z3c.jbot'])
