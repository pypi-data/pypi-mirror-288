from setuptools import setup, find_packages

setup(
    name='seiryu',
    version='0.8',
    packages=find_packages(),
    description='The Pinnacle of Advanced Hash Generation and Cryptographic Precision',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Veilwr4ith',
    author_email='hidetheveil@gmail.com',
    url='https://github.com/veilwr4ith/Seiryu',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'numpy',
        'argon2',
        'argon2-cffi',
        'bcrypt',
        'passlib',
        'siphashc',
        'spookyhash',
        'uuid',
        'xxhash',
        'argon2-cffi-bindings',
        'cffi'
    ],
    entry_points={
        'console_scripts': [
            'seiryu=seiryu.main:main',
        ],
    },
)
