from setuptools import setup

setup(
    name='pltwal',
    version='0.1.0',    
    description='Python package that uses pywal color scheme for matplotlib',
    url='',
    author='Sebastian Wohlrab',
    author_email='sebastian.wohlrab@wohlrab.de',
    license='GNUv3',
    packages=['pltwal'],
    install_requires=['numpy',
                      'matplotlib',
                      'pywal',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.12',
    ],
)

