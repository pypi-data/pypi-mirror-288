from setuptools import setup, find_packages



# Read the contents of your requirements file
with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='HPW_Tracing',
    version='0.2.0',
    packages=find_packages(),
    license='MIT',
    author='Peng Xie',
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    install_requires=required,
)



