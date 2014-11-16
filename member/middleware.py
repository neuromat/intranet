from django.http import HttpResponseRedirect

import re


class PasswordChangeMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated() and re.match(r'^/admin/?', request.path) and \
                not re.match(r'^/admin/password_change/?', request.path) and \
                not re.match(r'^/logout/?', request.path) and not request.user.is_superuser:

            profile = request.user.investigator
            if profile.force_password_change:
                return HttpResponseRedirect('/admin/password_change/')