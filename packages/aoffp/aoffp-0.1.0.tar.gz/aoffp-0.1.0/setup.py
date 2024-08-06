import setuptools

setuptools.setup(
    name='aoffp',
    version='0.1.0',
    packages=['ffp',],
    license='MIT',
    description = 'Python sdk for ffp',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'young',
    author_email = '',
    install_requires=['aodotpy'],
    url = 'https://github.com/permadao/ffp/tree/develop/sdk/python',
    download_url = '',
    # scripts=['bin/ffp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
