# This file is part of Moksha.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The Moksha Feed Tree Controller

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

import moksha
import moksha.utils
import logging

from tg import expose, tmpl_context
from pylons import cache
from orbited import json
from kitchen.text.converters import to_unicode

from moksha.lib.base import Controller
from mdemos.feeds.widgets import feed_entries_tree, moksha_feedreader

from tg import expose, validate
from formencode import validators

log = logging.getLogger('moksha.hub')

class FeedController(Controller):

    @expose('mako:mdemos.feeds.templates.index')
    @validate({'name': validators.UnicodeString()})
    def index(self, name='world', *args, **kw):
        return dict(name=name)

    @expose()
    def init_tree(self, key, fresh=False, **kw):
        c = cache.get_cache('feeds')
        if fresh:
            return self._get_feed_titles(fresh=fresh)
        else:
            return c.get_value(key='feed_titles',
                               createfunc=self._get_feed_titles,
                               expiretime=3600)

    def _get_feed_titles(self, fresh=False):
        results = []
        for feed in moksha.utils.feed_storage.keys():
            if not feed:
                raise Exception('None feed?!')
            if fresh:
                print "Getting fresh data"
                feed_data = moksha.utils.feed_cache.fetch(feed)
            else:
                print "Getting cached data"
                timestamp, feed_data = moksha.utils.feed_storage[feed]
            if not feed_data:
                log.debug("no feed_data, refetching")
                #feed_data = moksha.utils.feed_cache.fetch(feed)
                #if not feed_data:
                #    log.debug("NO FEED DATA AFTER FRESH FETCH!!!!")
                continue
            channel = feed_data.get('channel')
            if not channel:
                continue
            title = channel.get('title')
            results.append({
                'title': title,
                'key': feed,
                'isLazy': False,
                'isFolder': True,
                })
        return json.encode(results)

    @expose()
    def get_feed(self, key, *args, **kw):
        if '::' in key:
            url, title = key.split('::')
            for entry in moksha.utils.feed_storage[url][1]['entries']:
                content = entry.get('content', entry.get('summary'))
                content = '<span style="line-height:100%%;">%s</span>' % content
                if entry['title'] == title:
                    return json.encode([{'title': content, 'isLazy': False}])
            raise Exception("Cannot find entry by title: %s" % title)

        feed = moksha.utils.feed_storage[key][1]
        entries = []
        for entry in feed['entries']:
            entries.append({
                'title': entry.get('title'),
                'isLazy': True,
                'isFolder': True,
                'key': "%s::%s" % (key, entry.get('title')),
                })
        return json.encode(entries)

    @expose('mako:moksha.templates.widget')
    def get_entries(self, key, **kw):
        tmpl_context.widget = feed_entries_tree
        feed = moksha.utils.feed_storage[key][1]
        entries = []
        for entry in feed['entries']:
            entries.append({
                'title': entry.get('title'),
                'isLazy': False,
                'isFolder': False,
                'rootVisible': False,
                'key': "%s::%s" % (key, entry.get('title','').replace(' ','')),
                })
        return dict(options={'tree_children': entries})

    @expose()
    def get_entry(self, key, **kw):
        if '::' in key:
            url, title = key.split('::')
            for entry in moksha.utils.feed_storage[url][1]['entries']:
                content = entry.get('content', entry.get('summary'))
                if isinstance(content, list):
                    if isinstance(content[0], dict) and \
                       content[0].has_key('value'):
                        content = content[0]['value']
                content = """
                    <blockquote><h3><a href="%s">%s</a></h3><br/>%s</blockquote>
                """ % (entry.get('link', url), entry['title'], content)
                if entry['title'].replace(' ', '') == to_unicode(title):
                    return content
            raise Exception("Cannot find entry by title: %s" % title)
        else:
            raise Exception("Invalid entry key: %r" % key)
