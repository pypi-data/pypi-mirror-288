from setuptools import setup, find_packages

setup(
    name='ChartSmith',
    version='0.1.2',
    author='Tully OLeary',
    author_email='tullyro@gmail.com',
    description='A package for creating well-formatted, well-labeled visualizations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tullyoleary/ChartSmith',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.0.0',
        'seaborn>=0.11.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
