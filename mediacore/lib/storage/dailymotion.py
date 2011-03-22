# This file is a part of MediaCore, Copyright 2009 Simple Station Inc.
#
# MediaCore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MediaCore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import re
import simplejson

from urllib import urlencode
from urllib2 import Request, urlopen, URLError

from mediacore import USER_AGENT
from mediacore.lib.filetypes import VIDEO
from mediacore.lib.i18n import N_
from mediacore.lib.storage import EmbedStorageEngine
from mediacore.lib.uri import StorageURI

log = logging.getLogger(__name__)

class DailyMotionStorage(EmbedStorageEngine):

    engine_type = u'DailyMotionStorage'
    """A uniquely identifying unicode string for the StorageEngine."""

    default_name = N_(u'Daily Motion')

    url_pattern = re.compile(
        r'^(http(s?)://)?(\w+\.)?dailymotion.com/video/(?P<id>[^_\?&#]+)_'
    )
    """A compiled pattern object that uses named groupings for matches."""

    def _parse(self, url, **kwargs):
        """Return metadata for the given URL that matches :attr:`url_pattern`.

        :type url: unicode
        :param url: A remote URL string.

        :param \*\*kwargs: The named matches from the url match object.

        :rtype: dict
        :returns: Any extracted metadata.

        """
        id = kwargs['id']
        data_url = 'http://www.dailymotion.com/services/oembed?' + \
            urlencode({'format': 'json', 'url': url})

        headers = {'User-Agent': USER_AGENT}
        req = Request(data_url, headers=headers)

        try:
            temp_data = urlopen(req)
            try:
                data = simplejson.load(temp_data)
            finally:
                temp_data.close()
        except URLError, e:
            log.exception(e)
            data = {}

        return {
            'unique_id': id,
            'display_name': unicode(data.get('title', u'')),
            'thumbnail_url': data.get('thumbnail_url', None),
            'type': VIDEO,
        }

    def get_uris(self, media_file):
        """Return a list of URIs from which the stored file can be accessed.

        :type media_file: :class:`~mediacore.model.media.MediaFile`
        :param media_file: The associated media file object.
        :rtype: list
        :returns: All :class:`StorageURI` tuples for this file.

        """
        uid = media_file.unique_id
        play_url = 'http://www.dailymotion.com/embed/video/%s' % uid
        web_url = 'http://www.dailymotion.com/video/%s' % uid
        return [
            StorageURI(media_file, 'dailymotion', play_url, None),
            StorageURI(media_file, 'www', web_url, None),
        ]

EmbedStorageEngine.register(DailyMotionStorage)
