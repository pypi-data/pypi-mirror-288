from setuptools import setup, find_packages

setup(
    name='vector_qjszm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='ZhouQiang',
    author_email='zhou_qiang98@163.com',
    description='A simple 2D vector class',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZhouQiang19980220/Vertor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)