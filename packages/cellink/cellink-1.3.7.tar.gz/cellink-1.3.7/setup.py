import setuptools
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from os.path import join

str_version = '1.3.7'

def configuration(parent_package='', top_path=''):
    config = Configuration(None, parent_package, top_path)

    pkglist = setuptools.find_packages()
    for i in pkglist:
        config.add_subpackage(i)
    config.add_data_files(join('assets', 'imgs', '*.png'))
    config.add_data_files(join('README.md'))

    return config

if __name__ == '__main__':
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(
        configuration=configuration,
        name='cellink',
        version=str_version,
        description='An easy-to-use engine that allows python programmers to code with Chain of Responsibility Pattern',
        author='Zhai Menghua',
        author_email='viibridges@gmail.com',
        license='Apache 2.0',
        zip_safe=False,
        install_requires=['graphviz', 'numpy'],
        python_requires='>=3',
        long_description=long_description,
        long_description_content_type="text/markdown",
        # 如果有项目网址，取消注释并填写
        # url='https://github.com/yourusername/cellink',
    )
