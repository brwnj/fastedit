from setuptools import setup


setup(
    name='fastedit',
    version='0.1.4',
    url='http://github.com/brwnj/fastedit',
    license='MIT',
    author='Joe Brown',
    author_email='brwnjm@gmail.com',
    description='Quickly alter the headers of a manageable number of fasta entries using a CSV.',
    long_description=__doc__,
    py_modules=['fastedit'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        fastedit=fastedit:main
    '''
)
