from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _


@login_required
def display_documents(request):
    if request.user.has_perm('custom_auth.create_documents'):
        if 'suit' in settings.INSTALLED_APPS:
            return render(request, 'documents/documents_suit.html')
        else:
            return render(request, 'documents/documents.html')
    else:
        messages.warning(request, _("You don't have permission to access this page."))
        return redirect(reverse('admin:index'))


@login_required
def display_reports(request):
    if request.user.has_perm('custom_auth.view_reports'):
        if 'suit' in settings.INSTALLED_APPS:
            return render(request, 'report/reports_suit.html')
        else:
            return render(request, 'report/reports.html')
    else:
        messages.warning(request, _("You don't have permission to access this page."))
        return redirect(reverse('admin:index'))


@login_required
def display_add_content(request):
    if request.user.has_perm('custom_auth.add_content'):
        if 'suit' in settings.INSTALLED_APPS:
            return render(request, 'add_content/add_content_suit.html')
        else:
            return render(request, 'add_content/add_content.html')
    else:
        messages.warning(request, _("You don't have permission to access this page."))
        return redirect(reverse('admin:index'))