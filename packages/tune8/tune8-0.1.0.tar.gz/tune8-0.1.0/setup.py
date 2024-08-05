from setuptools import setup, find_packages

setup(
    name='tune8',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    entry_points={
        'console_scripts': [
            'tune8=tune8.app:run_app',
        ],
    },
    author='Naser Jamal',
    author_email='naser.dll@hotmail.com',
    description='A dashboard to work with Fine-tune JSONL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/naserjamal/tune8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)