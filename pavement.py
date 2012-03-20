# -*- coding: utf-8 -*-
from paver.easy import *
from paver.setuputils import (setup, find_package_data, find_packages,
                              install_distutils_tasks)
install_distutils_tasks()
from moksha.lib.paver_tasks import *

options(
    setup=Bunch(
        name="mdemos.feeds",
        version="0.1",
        release="1",
        url="http://moksha.fedorahosted.org",
        description="Describe your package here",
        license="ASL 2.0",
        long_description="",
        author="",
        author_email="",
        rpm_name='moksha-feeds',
        packages=find_packages(),
        package_data=find_package_data(),
        namespace_packages=[
            'mdemos',
        ],
        install_requires=[
            "moksha>=0.7.0a",
            "tw2.jqplugins.dynatree",
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
    ),
)
