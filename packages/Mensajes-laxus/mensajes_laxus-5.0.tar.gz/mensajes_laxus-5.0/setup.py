from setuptools import setup, find_packages

setup(
    name='Mensajes-laxus',
    version= '5.0',
    description='paquete para saludos y despedidas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Elias Arias Muñoz',
    author_email='eaarias320@gmail.com',
    url='',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[ package.strip() for package in open("requirements.txt").readlines() ],

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities'
    ]
)