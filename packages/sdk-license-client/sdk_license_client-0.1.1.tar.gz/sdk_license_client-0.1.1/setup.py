import os
import sys
from pathlib import Path

from setuptools import find_packages, setup, Command, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from shutil import rmtree
from setuptools.command.build import build

SRC_DIR = "sdk_license_client"
MODULE_NAME = 'sdk_license_client'
VERSION = '0.1.1'

ROOTPATH = os.path.abspath(os.path.dirname(__file__))
IGNORE_FILES = [
    "__init__.py",
]

with open("README.md", "r") as fh:
    long_description = fh.read()


def output(s: str):
    """
    控制台输出.
    """
    sys.stdout.write('\033[1m{0}\033[0m'.format(s) + '\n')
    sys.stdout.flush()  # 确保内容被及时输出


def scan_dir(dir_path, files=None):
    if files is None:
        files = []
    for f in os.listdir(dir_path):
        if f in IGNORE_FILES:
            continue
        path = os.path.join(dir_path, f)
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(path.replace(os.path.sep, ".")[:-3])
        elif os.path.isdir(path):
            scan_dir(path, files)
    return files


def make_extension(ext_name):
    ext_path = ext_name.replace(".", os.path.sep) + ".py"
    return Extension(ext_name, [ext_path], include_dirs=["."])


def delete_files(dir_path: Path, extensions: set):
    """
    删除指定目录中的文件，依据文件扩展名列表。
    """
    for f in dir_path.iterdir():
        if f.name in IGNORE_FILES:
            continue
        if f.is_file() and f.suffix[1:] in extensions:
            f.unlink()
        elif f.is_dir():
            delete_files(f, extensions)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'publish the package.'
    user_options = []

    def initialize_options(self):
        """
        初始化选项
        :return:
        """
        pass

    def finalize_options(self):
        """
        检查和处理选项
        :return:
        """
        pass

    def run(self):
        try:
            output('Removing previous builds…')
            rmtree(os.path.join(ROOTPATH, 'dist'))
        except OSError:
            pass

        output('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))  # sys.executable 为 Python 解释器的路径

        output('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        output('Clean....')
        os.system(f'rm -rf sdk_license_client.egg-info dist build')
        sys.exit()


class BuildExtCommand(build_ext):

    def run(self):
        super(BuildExtCommand, self).run()
        delete_files(Path(MODULE_NAME), extensions={'c'})


class BuildCommand(build):

    def run(self):
        super(BuildCommand, self).run()
        print("#" * 20)
        print(self.build_lib)
        build_path = Path(os.path.join(self.build_lib, MODULE_NAME))
        delete_files(build_path, extensions={'py'})


if __name__ == '__main__':
    ext_names = scan_dir(SRC_DIR)
    extensions = [make_extension(name) for name in ext_names]
    setup(
        name=MODULE_NAME,
        version=VERSION,
        author="alan",
        author_email="al6nlee@gmail.com",
        description="license的客户端",
        long_description=long_description,  # 项目的详细描述，会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
        long_description_content_type="text/markdown",
        url="https://github.com/al6nlee/sdk_license_client",
        packages=find_packages(exclude=('tests', 'tests.*')),  # 指定最终发布的包中要包含的packages
        ext_modules=cythonize(extensions),
        license='MIT License',  # 指定许可证类型
        classifiers=[
            "Intended Audience :: Developers",  # 目标用户
            'License :: OSI Approved :: MIT License',  # 许可证类型
            "Programming Language :: Python :: 3",  # 支持的 Python 版本
            "Topic :: Software Development"
        ],
        install_requires=[],  # 项目依赖哪些库(内置库就可以不用写了)，这些库会在pip install的时候自动安装
        python_requires='>=3.8',
        package_data={  # 默认情况下只打包py文件，如果包含其它文件比如.so格式，增加以下配置
            MODULE_NAME: [
                "*.py",
                "*.so",
            ]
        },
        cmdclass={
            'build_ext': BuildExtCommand,  # 构建 C 扩展模块
            'build': BuildCommand,  # 安装包到 Python 环境
            'push': UploadCommand,  # python3 setup.py push 触发，使用 twine
        },
    )
