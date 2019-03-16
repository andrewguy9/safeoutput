from setuptools import setup

tests_require = ['tox', 'pytest']

setup(
    name='safeoutput',
    version='1.0',
    description='Tempfile wrapper to ensure output is either complete, or empty',
    long_description='Tool to facilitate console script output redirection. When scripts run, often they have an output file option. If no output option is specified, its common to write to stdout. Its common to use tempfiles as output, and then rename the tempfile to the output name as the last step of the program so that the flip of output is atomic and partial/truncated/corrupt output is not confused as successful output. This is especially true when dealing with make, as exiting with error will stop make, but subsequent runs will assume that partial output files left in the workspace are complete.',
    url='http://github.com/andrewguy9/safeoutput',
    author='andrew thomson',
    author_email='athomsonguy@gmail.com',
    license='MIT',
    packages=['safeoutput'],
    install_requires=['future'],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points={'console_scripts': ['safeoutput = safeoutput:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Filesystems',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=True)
