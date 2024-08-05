from setuptools import setup, find_packages

setup(
    name="seiryu",
    version="1.0.18",
    packages=['seiryu'],
    install_requires=[
        'argon2',
        'argon2-cffi',
        'bcrypt',
        'numpy',
        'passlib',
        'siphashc',
        'spookyhash',
        'uuid',
        'xxhash',
        'argon2-cffi-bindings',
        'cffi',
    ],
    entry_points={
        'console_scripts': [
            'seiryu=seiryu.seiryu:main',
        ],
    },
    author="Veilwr4ith",
    author_email="hacktheveil@gmail.com",
    description="The Pinnacle of Advanced Hash Generator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/veilwr4ith/Seiryu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)

