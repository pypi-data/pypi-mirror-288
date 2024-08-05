from setuptools import setup

setup(
    name = "hpt-robot",
    version = "0.0.1",
    description='evaluating HPTs for robotics',
    url='https://liruiw.github.io/hpt',
    author='Lirui Wang',
    author_email='liruiw@mit.edu',
    license='MIT',
    packages=['hpt'],
    install_requires=["setuptools>=61.0",
                      ],

    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    ],
)