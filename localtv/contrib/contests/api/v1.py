# Miro Community - Easiest way to make a video website
#
# Copyright (C) 2009, 2010, 2011, 2012 Participatory Culture Foundation
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

from tastypie import fields
from tastypie import http
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource
from tastypie.utils.mime import build_content_type

from localtv.api.v1 import api, UserResource, VideoResource
from localtv.contrib.contests.authorization import UserAuthorization
from localtv.contrib.contests.models import Contest, ContestVote, ContestVideo


class ContestResource(ModelResource):
    votes = fields.ToManyField(
                'localtv.contrib.contests.api.v1.ContestVoteResource',
                'votes')
    videos = fields.ToManyField(VideoResource, 'videos')

    class Meta:
        queryset = Contest.objects.filter(site=settings.SITE_ID)


class ContestVideoResource(ModelResource):
    contest = fields.ToOneField(ContestResource, 'contest')
    video = fields.ToOneField(VideoResource, 'video')
    added = fields.DateTimeField('added')
    upvotes = fields.IntegerField()
    downvotes = fields.IntegerField()
    
    def dehydrate_upvotes(self, bundle):
        return bundle.obj.contestvote_set.filter(vote=ContestVote.UP).count()
    
    def dehydrate_downvotes(self, bundle):
        return bundle.obj.contestvote_set.filter(vote=ContestVote.DOWN).count()

    class Meta:
        queryset = ContestVideo.objects.filter(contest__site=settings.SITE_ID)


class ContestVoteResource(ModelResource):
    contestvideo = fields.ToOneField(ContestVideoResource, 'contestvideo')
    user = fields.ToOneField(UserResource, 'user')
    vote = fields.IntegerField('vote')

    def _handle_error(self, request, error_message, response_class=http.HttpForbidden):
        data = {
            "error_message": error_message,
        }
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        response = response_class(content=serialized,
                            content_type=build_content_type(desired_format))
        raise ImmediateHttpResponse(response)

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Creates a contest-vote object after ensuring that the user is set to
        the currently logged-in user, that the vote they are registering is
        allowed, and that they have not exceeded their vote count.

        """

        # Extract relevant data.
        contestvideo = ContestVideoResource().get_via_uri(bundle.data['contestvideo'])
        contest = contestvideo.contest
        video = contestvideo.video
        vote_value = int(bundle.data['vote'])

        # Verify authenticated user.
        if hasattr(request, 'user') and request.user.is_authenticated():
            kwargs['user'] = request.user
        else:
            self._handle_error(request,
                               'User must be logged-in to vote.')

        # Check vote is permissible.
        permissible_votes = (1, -1) if contest.allow_downvotes else (1,)
        if vote_value not in permissible_votes:
            self._handle_error(request,
                               'Vote value %d not permitted.' % vote_value)

        # Check vote counts.
        if contest.votes_per_user is not None:
            user_vote_count = ContestVote.objects.filter(
                                                contestvideo__contest=contest,
                                                user=request.user).count()
            if user_vote_count + 1 > contest.votes_per_user:
                self._handle_error(request,
                                   'Users may only vote %d times in %s.' %
                                   (contest.votes_per_user, contest.name))

        # Since everything checks out, go ahead and create the vote.
        return super(ContestVoteResource, self).obj_create(bundle,
                                                           request=request,
                                                           **kwargs)

    class Meta:
        queryset = ContestVote.objects.filter(
                                 contestvideo__contest__site=settings.SITE_ID)
        authorization = UserAuthorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'contestvideo': ALL_WITH_RELATIONS
        }
        always_return_data = True


api.register(ContestResource())
api.register(ContestVideoResource())
api.register(ContestVoteResource())