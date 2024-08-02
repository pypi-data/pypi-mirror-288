import os
from setuptools import setup, find_packages

setup(
    name='phylodeep_data_bdss',
    packages=find_packages(),
    include_package_data=True,
    package_data={'phylodeep_data_bdss': [os.path.join('large', '*.csv.xz'),
                                          os.path.join('..', 'README.md')]},
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    version='0.2',
    description='Data needed for CI computation with Birth-Death model with superspreading (BDSS) in [PhyloDeep](https://github.com/evolbioinfo/phylodeep).',
    author='Jakub Voznica',
    author_email='jakub.voznica@pasteur.fr',
    maintainer='Anna Zhukova',
    maintainer_email='anna.zhukova@pasteur.fr',
    url='https://github.com/evolbioinfo/phylodeep_data_bdss',
    keywords=['phylodeep', 'confidence intervals', 'birth-death with superspreading'],
    python_requires='>=3.8',
    install_requires=['pandas>=1.0.0'],
    entry_points={
        'console_scripts': [
            'bdss_ci_paths = phylodeep_data_bdss:main',
        ]
    },
)
