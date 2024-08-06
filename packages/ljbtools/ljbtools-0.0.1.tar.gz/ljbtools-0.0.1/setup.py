from setuptools import setup, find_packages

setup(
    name='ljbtools',
    version='0.0.1',
    author='Jianbin Li',
    author_email='491256499@qq.com',
    description='personal package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Jianbin-Li/ljbtools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
