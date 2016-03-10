from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class AuthorizationMiddleware(object):

    # Check if client IP is allowed
    def process_request(self, request):
        if request.user.is_authenticated():
            return None

        # except authorization pages
        if request.path in reverse('account_login'):
            return None

        return redirect(reverse('account_login'))
