# Copyright 2012 - Participatory Culture Foundation
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

from localtv.contrib.contests.tests.base import BaseTestCase
from localtv.contrib.contests.forms import ContestAdminForm

class ContestAdminFormUnit(BaseTestCase):

    def test_create(self):
        """
        Submitting a new form creates a new contest.
        """
        data = {
            'name': 'Test Name',
            'description': 'Test Description',
            'votes_per_user': 2,
            'allow_downvotes': True,
            'submissions_open': True,
            'voting_open': True,
            'display_vote_counts': True,
            'detail_columns': [1,2,3],
            }
        form = ContestAdminForm(data)
        self.assertTrue(form.is_valid(), getattr(form, 'errors', None))

        contest = form.save()
        for key, value in data.items():
            if key == 'detail_columns':
                self.assertEqual(contest.detail_columns, ','.join(
                        str(v) for v in value))
            else:
                self.assertEqual(getattr(contest, key), value,
                                 '%r key, %r != %r' % (
                        key, getattr(contest, key), value))

    def test_invalid(self):
        """
        Submitting a form which is missing some data doesn't validate.
        """
        data = {
            'name': 'Test Name',
            }
        form = ContestAdminForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.keys(), ['detail_columns'])

    def test_update(self):
        """
        Submitting a form given an existing instance updates that
        instance.
        """
        contest = self.create_contest()
        data = {
            'name': 'Test Name',
            'description': 'Test Description',
            'votes_per_user': 2,
            'allow_downvotes': True,
            'submissions_open': True,
            'voting_open': True,
            'display_vote_counts': True,
            'detail_columns': [1, 2, 3],
            }
        form = ContestAdminForm(data, instance=contest)
        self.assertTrue(form.is_valid(), getattr(form, 'errors', None))

        contest = form.save()
        for key, value in data.items():
            if key == 'detail_columns':
                self.assertEqual(contest.detail_columns, ','.join(
                        str(v) for v in value))
            else:
                self.assertEqual(getattr(contest, key), value,
                                 '%r key, %r != %r' % (
                        key, getattr(contest, key), value))

