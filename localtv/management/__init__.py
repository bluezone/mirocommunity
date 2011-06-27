# Copyright 2009 - Participatory Culture Foundation
# 
# This file is part of Miro Community.
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

"""
Creates the default SiteLocation object.
"""
import datetime

from django.db.models import signals
from django.contrib.auth.models import User

from localtv import models as localtv_app

TWO_MONTHS = datetime.timedelta(days=62)

def site_too_old():
    if User.objects.order_by('-last_login').values_list(
        'last_login', flat=True)[0] + TWO_MONTHS < datetime.datetime.now():
        return True
    else:
        return False

