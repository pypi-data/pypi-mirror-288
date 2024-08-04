from setuptools import setup, find_packages

setup(
    name='helix-beta',
    version='1.0.2024-3',
    description='So simple, its criminal',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='zeroth.bat@gmail.com',
    url='https://github.com/Zero-th/Zero-th',
    packages=find_packages(),
    package_data={"helix": ['assets/*']},
    install_requires=[
        'pygame-ce',
        'Swarm-ECS',
        'moderngl',
        'glfw',
        'numpy',
        'Pyglm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
