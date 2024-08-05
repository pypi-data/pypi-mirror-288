from setuptools import setup, find_packages

setup(
    name='airport-manager',
    version='0.2.23',  # Updated version number
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich',
        'click',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'airport-manager=airport_manager.cli:cli',
        ],
    },
    author='Shubh Thorat',
    author_email='reapers-arras.0y@icloud.com',
    description='Airport Manager: One-stop shop for all airport management needs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/itsjustshubh/airport_manager',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
