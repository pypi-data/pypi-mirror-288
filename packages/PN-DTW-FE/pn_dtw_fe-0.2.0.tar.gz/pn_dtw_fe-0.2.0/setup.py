from setuptools import setup, find_packages

setup(
    name='PN_DTW_FE',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'pandas==1.4.3',
        'numpy==1.22.4',
        'scipy==1.7.3',
        'fastdtw==0.3.4',
    ],
    entry_points={
        'console_scripts': [
            'PNdtwFE = PN_DTW_FE.main:main',
        ],
    },
    author='Md Khairul Islam, Prof Hairong Wei',
    author_email='hairong@mtu.edu',
    description='A package for gene expression analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/PN_DTW_FE',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.10.3',
)
