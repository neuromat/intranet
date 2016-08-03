from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.translation import activate, LANGUAGE_SESSION_KEY


@login_required
def language_change(request, language_code):
    activate(language_code)
    request.session[LANGUAGE_SESSION_KEY] = language_code

    return HttpResponseRedirect(request.GET['next'])
