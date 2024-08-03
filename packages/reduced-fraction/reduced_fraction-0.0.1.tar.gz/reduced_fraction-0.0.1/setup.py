import setuptools
with open('README.md',encoding='utf-8') as f:
    long_des = f.read()
setuptools.setup(
    name='reduced_fraction',
    version='0.0.1',
    author='LightingLong',
    author_email='17818883308@139.com',
    description='计算最简分数的库',
    long_description=long_des,
    url='https://github.com/longliangzhe/reduced_fraction',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.0.1'
)