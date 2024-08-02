from setuptools import setup, find_packages

setup(
    name='babytalk',
    version='2.1.0',
    packages=find_packages(),
    # Removed tkinter from install_requires
    install_requires=[],  
    description='A library to simplify Python programming for young learners using natural language commands.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mutaib-yye/babytalk',
    author='Mutaib',
    author_email='mutaibrather333@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',  # Added a classifier for the target audience
        'Topic :: Education :: Computer Aided Instruction (CAI)', # Added a classifier for the topic
        'Development Status :: 4 - Beta'  # Indicate the development status (beta)
    ],
    python_requires='>=3.6',
)
