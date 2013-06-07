import os

from setuptools import setup

version = __import__('antibrute').get_version()

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-antibrute',
    version=version,
    packages=['antibrute'],
    include_package_data=True,
    license='MIT License',
    description='Django app for stopping brute force attack \
                against login page.',
    long_description=README,
    author='Maulik Kataria',
    author_email='maulik.kataria@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
