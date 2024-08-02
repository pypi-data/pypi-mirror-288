from setuptools import setup, find_packages

setup(
    name='babytalk',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        # Add any other dependencies here, but do not include 'tkinter'
    ],
    description='A library to simplify Python programming for young learners using natural language commands.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mutaib-yye/babytalk',  # Update this with the URL to your repository
    author='Mutaib',
    author_email='mutaibrather333@gmail.com',  # Update this with your email
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
