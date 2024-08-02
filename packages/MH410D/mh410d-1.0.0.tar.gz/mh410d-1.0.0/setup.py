from setuptools import setup, find_packages

setup(
    name='MH410D',
    version='1.0.0',
    author='Artem-Darius Weber',
    author_email='neko-sensors@k-lab.su',
    description='MH410D CO2 UART/V out 0-10.00% VOL Sensor.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NekoSensors/MH410D',
    packages=find_packages(),
    install_requires=[
        "pyserial",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
