from setuptools import setup, find_packages

setup(
    name='hoadleyYaPu',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    author='Yash Purohit',
    author_email='yashpurohit1234@gmail.com',
    description='A package for Black-Scholes option pricing and implied volatility calculation(European Options only)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iam7pY/hoadleyYaPu',  # Replace with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
