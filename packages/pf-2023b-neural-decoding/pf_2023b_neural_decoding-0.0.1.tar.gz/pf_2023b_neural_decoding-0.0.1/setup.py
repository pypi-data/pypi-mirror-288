from setuptools import setup, find_packages

setup(
    name='pf_2023b_neural_decoding',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.4'
    ],
    author='Gonzalo Beade, Mila Langone, Santiago Hadad',
    author_email='gbeade@itba.edu.ar, mlangone@itba.edu.ar, shadad@itba.edu.ar',
    description="""
        A package containing all exported artifacts from the pf-2023b-neural-decoding final graduate project.
    """,
    url='https://bitbucket.org/itba/pf-2023b-neural-decoding/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
