import setuptools
with open('README.md','r',encoding='utf-8') as f:
    long_des = f.read()
setuptools.setup(
    name='suffix_expression',
    version='2024.8.2',
    author='Lighting Long',
    author_email='17818883308@139.com',
    description='后缀表达式处理库',
    long_description=long_des,
    url='https://github.com/longliangzhe/suffix_expression',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0.1'
)