from setuptools import setup, find_packages

setup(
    name='epsilon-client',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'python-dotenv',
    ],
    keywords='epsilon epsilon_atlas client, apache epsilon_atlas',
    include_package_data=True,
    author='xxx',
    author_email='xxxx@example.com',
    description='A package for reading data from CSV or XLS files and publishing to Apache Atlas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/khajievN/test-python/tree/release',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
