from setuptools import setup, find_packages

setup(
    name='imagecompression6',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'scikit-image',
        'matplotlib'
    ],
    description='Image compression using REIS algorithms',
    author='Katie Wen Ling Kuo',
    author_email='katie20030705@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
