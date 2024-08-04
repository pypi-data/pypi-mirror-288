from setuptools import setup

entry_point_script = "gbv.gbv:cli"
with open("gbv/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="gbv",  # PyPI上的包名
    packages=["gbv"],  # 包含的Python模块或子包
    version="0.1.2",  # 版本号
    author="PYmili",  # 作者
    author_email="mc2005wj@163.com",
    description="A package to get videos from Bilibili",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/PYmili/gbv",
    classifiers=[  # 可选，用于描述项目的元数据
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',  # 可选，指定支持的Python版本
    install_requires=[
        "beautifulsoup4",
        "bs4",
        "certifi",
        "charset-normalizer",
        "colorama",
        "fileid",
        "idna",
        "loguru",
        "lxml",
        "requests",
        "rookiepy",
        "setuptools",
        "soupsieve",
        "tqdm",
        "urllib3",
        "uuid",
        "win32-setctime",
    ],  # 可选，项目依赖的其他PyPI包
    entry_points={
        'console_scripts': [
            'gbv={}'.format(entry_point_script),  # 这里定义了命令行工具的名字及其入口
        ],
    },
)