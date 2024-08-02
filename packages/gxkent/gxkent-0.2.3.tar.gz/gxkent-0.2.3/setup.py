from setuptools import setup, find_packages

setup(
    name='gxkent',
    version='0.2.3',
    description='A way to use Great Expectations in Google Collab and other notebook environments.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/careset/GXKent',
    author='Fred Trotter',
    author_email='fred.trotter@careset.com',
    license='LICENSE.txt',
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
