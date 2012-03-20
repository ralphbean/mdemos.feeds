# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name="mdemos.feeds",
    version="0.1.0a",
    url="http://moksha.fedorahosted.org",
    description="Moksha Feeds App",
    license="ASL 2.0",
    long_description="",
    author="Luke Macken",
    author_email="lmacken@redhat.com",
    packages=['mdemos', 'mdemos.feeds'],
    namespace_packages=[
        'mdemos',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "moksha>=0.7.0a",
        "tw2.jqplugins.dynatree",
        "tw2.jqplugins.cookies",
    ],
    entry_points={
        'moksha.producer': (
            'feeds = mdemos.feeds.streams:MokshaFeedStream',
        ),
        'moksha.consumer': (
            'feeds = mdemos.feeds.consumer:MokshaFeedConsumer'
        ),
        'moksha.application': (
            'feeds = mdemos.feeds.controllers:FeedController'
        ),
        'moksha.widget': (
            'feeds = mdemos.feeds.widgets:moksha_feedreader'
        ),
    }
)
