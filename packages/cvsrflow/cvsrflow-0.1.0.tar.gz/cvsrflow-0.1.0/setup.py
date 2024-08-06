from setuptools import setup, find_packages

setup(
    name='cvsrflow',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    description='A library for capturing website screenshots and sending them to OpenAI API.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/cvsrflow',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
