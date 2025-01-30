from setuptools import setup, find_packages

setup(
    name='your-cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'your-cli-command=your_module:main_function',
        ],
    }
)