from setuptools import setup, find_packages

setup(
    name='fastapi-request-limit',
    version='0.1.0',
    description='A FastAPI decorator for rate limiting requests based on specified parameters.',
    author='Sqot0',
    author_email='kuvshinov556@gmail.com',
    url='https://github.com/sqot0/fastapi-request-limit',
    packages=find_packages(),
    install_requires=[
        'fastapi',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
