from setuptools import setup, find_packages

setup(
    name='gxkent',
    version='0.2.0',
    author='Fred Trotter',
    author_email='fred.trotter@careset.com',
    url='http://pypi.python.org/pypi/GXKent/',
    license='LICENSE.txt',
    description='An awesome package for GXKent.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'great-expectations>=0.18.0'
    ],
    packages=find_packages(),          # Packages to include
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
