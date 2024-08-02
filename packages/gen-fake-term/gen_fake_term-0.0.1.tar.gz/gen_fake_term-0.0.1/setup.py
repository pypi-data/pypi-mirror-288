from setuptools import setup, find_packages
from Cython.Build import cythonize
import os
from distutils.extension import Extension

# Make extensions for cythonize
def scandir(dir, files=[]):
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                files.append(filepath.replace(os.path.sep, '.')[:-3])
    return files

extra_compile_args = [
    '-O1',  # 调整大O优化等级
]

def makeExtension(extName):
    extPath = extName.replace('.', os.path.sep) + '.py'
    return Extension(
        extName,
        [extPath],
        include_dirs=['.'],
        extra_compile_args=extra_compile_args,
    )

pkg = "gen_fake_term"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=pkg,
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gen_fake_term=gen_fake_term.main:main',
        ],
    },
    author='mike',
    author_email='zhongscmike@joinwisdom.cn',
    description='Generate fake term from fwd data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)