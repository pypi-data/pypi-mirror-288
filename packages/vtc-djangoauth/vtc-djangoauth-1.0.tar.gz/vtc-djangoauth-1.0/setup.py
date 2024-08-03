from setuptools import setup

setup(
    name='vtc-djangoauth',
    version='1.0',
    packages=['authentication'],
    include_package_data=True,
    install_requires=['Django>=4.2'],
    author='Thamarai selvan',
    author_email='Thamarai.pmp@gmail.com',
    description='A Django app for authentication with jwt token',
    url='https://github.com/Thamaraiselvan5960/vtc_djangoauth',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
)