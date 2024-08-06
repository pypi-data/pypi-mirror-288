from setuptools import setup, find_packages

setup(
    name='cvsrflow',
    version='0.2.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    description='This is cvsrflow - a computer vision-based scrapping replacement technology developed by Exthalpy Technoligies.',
    author='Exthalpy',
    author_email='udit@exthalpy.com',
    url='https://exthalpy.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
