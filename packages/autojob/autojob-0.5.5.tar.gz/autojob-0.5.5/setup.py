import os

from setuptools import setup, find_packages

# with open("README.md") as f:
#     long_description = f.read()

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="autojob",
    version='0.5.5',
    description="Django customizes management pages based on APScheduler",
    keywords='autojob',
    long_description=README,
    long_description_content_type="text/markdown",
    author='zkrliumy',
    author_email='zkrliumy@163.com',
    url="https://github.com/lmycc/autojob",
    include_package_data=True,
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(include=('autojob',)),
    zip_safe=False,
    # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    install_requires=[
        'Django>=2.0',
        'djangorestframework>=3.7.0',
        'APScheduler',
        'django-redis',
    ],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django",
        "Framework :: Django :: 2",
        "Framework :: Django :: 3",
        "Framework :: Django :: 4",
    ],
)
