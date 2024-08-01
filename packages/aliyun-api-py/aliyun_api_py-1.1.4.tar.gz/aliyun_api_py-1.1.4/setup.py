import io
import os
from setuptools import setup

NAME = "aliyun-api-py"
DESCRIPTION = "一个简单的阿里云API Python封装库"
URL = "https://github.com/AkariRin/aliyun-api-py"
EMAIL = "akaririn1028@gmail.com"
AUTHOR = "Akari Rin"
REQUIRES_PYTHON = ">=3.6.0"
REQUIRED = ["requests", "pytz"]
EXTRAS = {}

root = os.path.abspath(os.path.dirname(__file__))

# 加载readme
with io.open(os.path.join(root, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

# 加载版本号
version = {}
with open(os.path.join(root, 'aliyun-api-py', '__version__.py')) as f:
    exec(f.read(), version)

setup(
    name=NAME,
    version=version["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["aliyun-api-py"],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
