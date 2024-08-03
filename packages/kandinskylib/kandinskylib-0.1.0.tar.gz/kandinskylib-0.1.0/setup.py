from setuptools import setup, find_packages

setup(
    name='kandinskylib',
    version='0.1.0',
    description='A library for interacting with Kandinsky AI image generation API',
    author='Read1dno',
    author_email='ef8ser@gmail.com',
    url='https://github.com/Read1dno/kandinskylib',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Pillow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
