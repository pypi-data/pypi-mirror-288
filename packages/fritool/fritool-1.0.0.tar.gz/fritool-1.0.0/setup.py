from setuptools import setup, find_packages

setup(
    name='frtool',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
    ],
    include_package_data=True,
    description='Multi-package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='5sigma',
    author_email='support@5sigma.co',
    url='https://github.com/5SigmaInc/frtool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)