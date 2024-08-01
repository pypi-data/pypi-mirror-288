import setuptools
from aestate.work.commands import __version__, __description__, __license__, __author_email__, __author__, \
    __project_name__, __url__, __issues__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = ['aestate', 'aestate.ajson', 'aestate.base', 'aestate.dbs', 'aestate.dbs._mssql', 'aestate.dbs._mysql',
            'aestate.exception', 'aestate.i18n', 'aestate.util', 'aestate.work', 'aestate.work.commands',
            'aestate.work.proxy', 'aestate.work.sql', 'aestate.work.xmlhandler']
print(setuptools.find_packages())

setuptools.setup(
    name=__project_name__,
    # 版本号
    version=__version__,
    # 作者名称
    author=__author__,
    # 作者邮箱
    author_email=__author_email__,
    # 说明文字
    description=__description__,
    # 描述文本
    long_description=long_description,
    # 描述类型
    long_description_content_type="text/markdown",
    # 项目链接
    url=__url__,
    # 项目连接
    project_urls={
        "Bug Tracker": __issues__,
    },
    # 许可证
    license=__license__,
    # 分类
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
    packages=packages,
    python_requires=">=3.7",
    install_requires=['prettytable', 'cryptography', 'psutil', 'DBUtils', 'simplejson'],
    entry_points={
        'console_scripts': [
            'aestate=aestate:start',
        ]
    },
)
