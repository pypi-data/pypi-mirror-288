import sys
import functools
import setuptools

if sys.version_info.major >= 3:
    open = functools.partial(open, encoding='utf8')

setuptools.setup(
    name='LogCollectionFormatter2',
    version='2.0alpha2',
    author='Unnamed great master',
    author_email='<gqylpy@outlook.com>',
    license='BSD 3-Clause',
    project_urls={
        'Source': 'https://github.com/2018-11-27/LogCollectionFormatter2'
    },
    description='''
        LogCollectionFormatter2 是一个专为Python应用程序设计的日志记录和消息队列工具库，
        提供强大功能，帮助开发者轻松追踪应用状态和发送日志消息到消息队列。
    '''.strip().replace('\n       ', ''),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['LogCollectionFormatter2'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=['gevent', 'kombu', 'Flask'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: Log Analysis',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)
