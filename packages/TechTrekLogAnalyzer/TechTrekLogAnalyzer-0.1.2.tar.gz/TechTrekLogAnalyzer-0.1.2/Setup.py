from setuptools import setup, find_packages

setup(
    name='TechTrekLogAnalyzer',
    version='0.1.2',
    packages=find_packages(),
   # description='A package to analyze and report on log file data.',
   # long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    author='Tech Trek Team',
    url='https://github.com/Durbace/TechTrekLogAnalyzer',
    install_requires=[
        'pandas',  
        'numpy'   
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
