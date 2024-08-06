import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='vbaProject',
    version='0.0.1',
    description='vba工具库，通过vbpip进行包管理。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='PyDa5',
    author_email='1174446068@qq.com',
    license='MIT',
    packages=[],
    include_package_data=True,  # 启用清单文件
)
