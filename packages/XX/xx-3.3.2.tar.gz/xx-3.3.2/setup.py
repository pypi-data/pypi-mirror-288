# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
"""
rm -rf dist/* && python setup.py sdist_wheel --universal && twine upload dist/* -u billsteve -p aaasss25 --verbose
"""

setup(
    name="XX",
    version="3.3.2",
    description=(
        "Python tools for myself(billsteve@126.com)"
    ),
    long_description="""
    ## Just Test, Just for myself! Not safe,not stable and will boom boom boom. ##
    
    Just like these:
        -  https://music.163.com/song?id=3949444&userid=319278554  
        -  https://music.163.com/song?id=474581010&userid=319278554  
        -  https://open.spotify.com/album/47wyCwrChF50ZTFNOuWx99  
        -  https://open.spotify.com/track/3oDFtOhcN08qeDPAK6MEQG  
    
    Changelog:
        ### 3.2.4
            -  增加base64编码和解码
        ### 3.1.0
            -  Scrapy->DM->CacheDM::CacheFileRequest, del response.certificate.
        ### 3.0.6
            -  add get_cache_file in Scrapy->DM->CacheDM::CacheFileRequest.
                Could cache file by CacheFileRequest if you don't set FUN_CACHE_FILE_PATH in setting.               
        ### 3.0.4
            - add get p domain    
    """,
    author='bill steve',
    author_email='billsteve@126.com',
    maintainer='bill steve',
    maintainer_email='billsteve@126.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/billsteve',

    install_requires=[
        "scrapy",
        "scrapyd",
        "scrapyd-client",
        "scrapy-redis",
        "pyquery",
        "redis",
        "requests",
        "pymysql",
        "sqlalchemy",
        "logzero",
        "happybase",
        "tld"
    ],

    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
