# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

 
setup(
    name="http_browser",
    version="1.1.1",
    author="jiaobenxiaozi",
    author_email="",
    description="浏览器助手",
 
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'DrissionPage' 
    ],
 
    python_requires='>=3.6',
    # entry_points={
    #     'console_scripts': [
    #         'dp = DrissionPage.commons.cli:main',
    #     ],
    # },
)
