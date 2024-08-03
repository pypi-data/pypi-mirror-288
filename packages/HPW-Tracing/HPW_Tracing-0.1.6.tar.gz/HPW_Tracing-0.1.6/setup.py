from setuptools import setup, find_packages



# Read the contents of your requirements file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='HPW_Tracing',
    version='0.1.6',
    packages=find_packages(),
    license='MIT',
    author='Peng Xie',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    install_requires=required,
)



