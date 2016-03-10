from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class AuthorizationMiddleware(object):

    def process_request(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated():
            return None

        # except authentication pages
        if '/account/' in request.path:
            return None

        # redirect to login
        return redirect(reverse('account_login'))
