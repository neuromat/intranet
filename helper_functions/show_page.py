from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _


@login_required
def display_documents(request):
    if request.user.has_perm('custom_auth.create_documents'):
        return render(request, 'documents/documents.html')
    else:
        messages.warning(request, _("You don't have permission to access this page."))
        return redirect(reverse('admin:index'))


# Maybe a little of cpd reports here
@login_required
def display_reports(request):
    if request.user.has_perm('custom_auth.view_reports'):
        return render(request, 'report/reports.html')
    else:
        messages.warning(request, _("You don't have permission to access this page."))
        return redirect(reverse('admin:index'))