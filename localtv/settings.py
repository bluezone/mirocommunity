# Miro Community - Easiest way to make a video website
#
# Copyright (C) 2011, 2012 Participatory Culture Foundation
#
# Miro Community is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Miro Community is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Miro Community.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings

#: The amount of time that the "popular videos" query is considered valid.
#: Default: 2 hours. (2 * 60 * 60 seconds)
POPULAR_QUERY_TIMEOUT =  getattr(settings, 'LOCALTV_POPULAR_QUERY_TIMEOUT',
                                 2 * 60 * 60)
ENABLE_ORIGINAL_VIDEO = not getattr(settings,
                                    'LOCALTV_DONT_LOG_REMOTE_VIDEO_HISTORY',
                                    None)
ENABLE_CHANGE_STAMPS = getattr(settings, 'LOCALTV_ENABLE_CHANGE_STAMPS', False)
SHOW_ADMIN_DASHBOARD = getattr(settings, 'LOCALTV_SHOW_ADMIN_DASHBOARD', True)
SHOW_ADMIN_ACCOUNT_LEVEL = getattr(settings, 'LOCALTV_SHOW_ADMIN_ACCOUNT_LEVEL',
                                   True)
USE_HAYSTACK = getattr(settings, 'LOCALTV_USE_HAYSTACK', True)

API_KEYS = {
    'vimeo_key': getattr(settings, 'VIMEO_API_KEY', None),
    'vimeo_secret': getattr(settings, 'VIMEO_API_SECRET', None),
    'ustream_key': getattr(settings, 'USTREAM_API_KEY', None)
}
