import os
import re

from setuptools import setup

package_regex = re.compile(r'.*__pycache__.*|.*docs.*')
dirs = [d[0] for d in os.walk('faust_tools')]
packages = [
    path.replace('/', '.') for path in dirs if not package_regex.match(path)
]
setup(
    name='faust-tools',
    version='1.0.4',
    description='Faust Tools',
    url='https://gitlab.com/is4res/faust-tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    license_files=('LICENSE',),
    author='Isares S.',
    author_email='isares.br@gmail.com',
    python_requires='>=3.9',
    packages=packages,
    include_package_data=True,
    install_requires=[
        'faust-streaming',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
)
