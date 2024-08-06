from setuptools import setup, find_packages

setup(
    name='utb_test_package',
    version='0.2.0',
    author='Artem Mikhaylov',
    author_email='utb404@gmail.com',
    description='Краткое описание вашего пакета',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/utb404',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
