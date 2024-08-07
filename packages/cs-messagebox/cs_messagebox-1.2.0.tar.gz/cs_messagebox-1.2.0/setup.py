from setuptools import setup, find_packages

setup(
    name='cs_messagebox',
    version='1.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow',
    ],
)
